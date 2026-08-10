#!/usr/bin/env python3
"""Discover and write conservative all-city schedule data.

The pipeline crawls only public official hospital pages at low frequency. It
promotes records to L1 only when a page contains strong schedule signals and a
table/list row has enough structure to identify department, doctor, date or
weekday, and time slot.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data-access-research"
FRONTEND_DIR = ROOT / "frontend-prototype"
REPORT_FILE = DATA_DIR / "all-city-crawl-report.json"
SCHEDULE_JS_FILE = FRONTEND_DIR / "all-city-schedule-data.js"
USER_AGENT = "Mozilla/5.0 registration-research/0.5"
MAX_FETCH_BYTES = 6_000_000

sys.path.insert(0, str(DATA_DIR))
from registry_parser import parse_all_city_registries  # noqa: E402


SCHEDULE_LINK_HINT = re.compile(r"(出诊|排班|门诊|专家|预约|挂号|schedule|clinic|doctor|visit)", re.I)
SCHEDULE_PAGE_HINT = re.compile(r"(出诊|排班|门诊安排|专家门诊|普通门诊|停诊|可预约|clinic|schedule)", re.I)
DATE_HINT = re.compile(r"(\d{4}[-/.年]\d{1,2}[-/.月]\d{1,2}日?|\d{1,2}[-/.月]\d{1,2}日?|星期[一二三四五六日天]|周[一二三四五六日天])")
SLOT_HINT = re.compile(r"(上午|下午|晚上|夜间|全天|午间)")
BAD_LINK_HINT = re.compile(r"(javascript:|#|tel:|mailto:|login|sitemap)", re.I)
SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b.*?</\1>", re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")


@dataclass
class FetchResult:
    url: str
    ok: bool
    status: int | None
    elapsed_ms: int
    text: str
    error: str = ""


class LinkParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.links: list[dict[str, str]] = []
        self._active_href = ""
        self._active_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key.lower(): value or "" for key, value in attrs}
        href = attr.get("href") or attr.get("data-href") or attr.get("src") or ""
        joined = " ".join([tag, *attr.values()])
        if href and SCHEDULE_LINK_HINT.search(joined) and not BAD_LINK_HINT.search(href):
            self.links.append({
                "url": urllib.parse.urljoin(self.base_url, href),
                "text": html.unescape(joined)[:160],
            })
        if tag == "a" and href:
            self._active_href = href
            self._active_text = []

    def handle_data(self, data: str) -> None:
        if self._active_href:
            self._active_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "a" or not self._active_href:
            return
        text = " ".join(" ".join(self._active_text).split())
        if text and SCHEDULE_LINK_HINT.search(text) and not BAD_LINK_HINT.search(self._active_href):
            self.links.append({
                "url": urllib.parse.urljoin(self.base_url, self._active_href),
                "text": text[:160],
            })
        self._active_href = ""
        self._active_text = []


class TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tables: list[list[list[str]]] = []
        self.captions: list[str] = []
        self._in_table = False
        self._in_caption = False
        self._in_row = False
        self._in_cell = False
        self._table: list[list[str]] = []
        self._caption_text: list[str] = []
        self._row: list[str] = []
        self._cell_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "table":
            self._in_table = True
            self._table = []
            self._caption_text = []
        elif self._in_table and tag == "caption":
            self._in_caption = True
        elif self._in_table and tag == "tr":
            self._in_row = True
            self._row = []
        elif self._in_row and tag in {"td", "th"}:
            self._in_cell = True
            self._cell_text = []

    def handle_data(self, data: str) -> None:
        if self._in_cell:
            self._cell_text.append(data)
        elif self._in_caption:
            self._caption_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self._in_cell:
            text = " ".join(" ".join(self._cell_text).split())
            self._row.append(html.unescape(text))
            self._in_cell = False
        elif tag == "caption" and self._in_caption:
            self._in_caption = False
        elif tag == "tr" and self._in_row:
            if any(self._row):
                self._table.append(self._row)
            self._in_row = False
        elif tag == "table" and self._in_table:
            if self._table:
                self.tables.append(self._table)
                caption = " ".join(" ".join(self._caption_text).split())
                self.captions.append(html.unescape(caption))
            self._in_table = False


def fetch(url: str, timeout: int) -> FetchResult:
    started = time.time()
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read(MAX_FETCH_BYTES)
            charset = response.headers.get_content_charset() or "utf-8"
            return FetchResult(url, True, response.status, int((time.time() - started) * 1000), raw.decode(charset, errors="replace"))
    except Exception as exc:  # noqa: BLE001
        status = exc.code if isinstance(exc, urllib.error.HTTPError) else None
        return FetchResult(url, False, status, int((time.time() - started) * 1000), "", str(exc))


def same_host_or_subpath(source_url: str, candidate_url: str) -> bool:
    source = urllib.parse.urlparse(source_url)
    candidate = urllib.parse.urlparse(candidate_url)
    return candidate.scheme in {"http", "https"} and candidate.netloc.lower() == source.netloc.lower()


def clean_text(raw_html: str) -> str:
    text = SCRIPT_STYLE_RE.sub(" ", raw_html)
    text = TAG_RE.sub(" ", text)
    return html.unescape(" ".join(text.split()))


def normalize_date(value: str) -> tuple[str, str]:
    value = value.replace("星期天", "星期日").replace("周天", "周日")
    weekday = re.search(r"(星期[一二三四五六日]|周[一二三四五六日])", value)
    weekday_text = weekday.group(1).replace("周", "星期") if weekday else ""
    date = re.search(r"(\d{4})[-/.年](\d{1,2})[-/.月](\d{1,2})日?", value)
    if date:
        return f"{int(date.group(1)):04d}-{int(date.group(2)):02d}-{int(date.group(3)):02d}", weekday_text
    month_day = re.search(r"(\d{1,2})[-/.月](\d{1,2})日?", value)
    if month_day:
        return f"{datetime.now().year:04d}-{int(month_day.group(1)):02d}-{int(month_day.group(2)):02d}", weekday_text
    return "", weekday_text


def looks_like_doctor_name(value: str) -> bool:
    if re.fullmatch(r"(上午|下午|晚上|夜间|全天|停诊|约满|可约|普通|专家|专科|门诊|星期[一二三四五六日]|周[一二三四五六日])", value.strip()):
        return False
    if re.search(r"(隔周|交替|轮流|待定|另行|暂停|节假日|详见|具体)", value):
        return False
    value = re.sub(r"(主任医师|副主任医师|主治医师|医师|教授|专家|普通|门诊|停诊|约满|上午|下午|晚上|夜间|全天)", " ", value)
    names = [item for item in re.split(r"[\s、,，/]+", value) if 2 <= len(item) <= 4 and re.search(r"[\u4e00-\u9fff]", item)]
    return bool(names)


def split_doctors(value: str) -> list[str]:
    cleaned = re.sub(r"(主任医师|副主任医师|主治医师|住院医师|教授|专家门诊|普通门诊)", " ", value)
    banned = {"上午", "下午", "晚上", "夜间", "全天", "停诊", "约满", "可约", "普通", "专家", "专科", "门诊"}
    return [
        item
        for item in re.split(r"[\s、,，/]+", cleaned)
        if 2 <= len(item) <= 4 and re.search(r"[\u4e00-\u9fff]", item) and item not in banned and not re.match(r"^(星期|周)", item)
        and not re.search(r"(隔周|交替|轮流|待定|另行|暂停|节假日|详见|具体)", item)
    ][:8]


def fetch_json(url: str, timeout: int) -> tuple[dict[str, Any] | None, FetchResult]:
    result = fetch(url, timeout)
    if not result.ok:
        return None, result
    try:
        return json.loads(result.text), result
    except json.JSONDecodeError as exc:
        return None, FetchResult(result.url, False, result.status, result.elapsed_ms, result.text, str(exc))


def flatten_womanhospital_depts(nodes: list[dict[str, Any]]) -> list[dict[str, str]]:
    leaves: list[dict[str, str]] = []
    for node in nodes:
        children = node.get("children") or []
        if children:
            leaves.extend(flatten_womanhospital_depts(children))
            continue
        dept = node.get("dept") or {}
        dept_type = str(dept.get("deptType") or node.get("deptCode") or "")
        dept_name = str(dept.get("deptTypeName") or node.get("deptName") or "")
        org_code = str(dept.get("orgCode") or node.get("areaCode") or "")
        if dept_type and dept_name and org_code:
            leaves.append({"deptType": dept_type, "deptTypeName": dept_name, "orgCode": org_code})
    return leaves


def parse_womanhospital_schedule_rows(
    rows: list[dict[str, Any]],
    hospital: dict[str, str],
    source_url: str,
    max_records: int,
    start_index: int,
) -> list[dict[str, Any]]:
    slot_map = {"1": "上午", "2": "下午", "3": "晚上", "4": "夜间"}
    state_map = {"0": "可预约", "1": "停诊"}
    records: list[dict[str, Any]] = []
    for row in rows:
        if len(records) >= max_records:
            break
        raw_date = str(row.get("schDate") or "")
        visit_date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}" if re.fullmatch(r"\d{8}", raw_date) else raw_date
        doc_name = str(row.get("docName") or "").strip() or str(row.get("deptName") or row.get("deptTypeName") or "普通门诊")
        dept_name = str(row.get("deptName") or row.get("deptTypeName") or "未标注科室")
        num_remain = str(row.get("numRemain") or "")
        num_count = str(row.get("numCount") or "")
        records.append({
            "id": f"{hospital['id']}-api-{start_index + len(records)}",
            "city": hospital["city"],
            "hospitalId": hospital["id"],
            "hospitalName": hospital["name"],
            "campusName": str(row.get("orgCode") or hospital.get("shortName") or hospital["name"]),
            "departmentName": dept_name,
            "standardDepartment": "",
            "subDepartment": str(row.get("deptTypeName") or dept_name),
            "doctorName": doc_name,
            "doctorSpecial": str(row.get("docDesc") or ""),
            "professionalTitle": str(row.get("title") or ""),
            "clinicLevel": str(row.get("deptId") or "").split("-", 1)[0],
            "visitDate": visit_date,
            "dateLabel": raw_date,
            "weekday": "",
            "displayDate": visit_date or raw_date,
            "timeSlot": slot_map.get(str(row.get("ampm") or ""), str(row.get("ampm") or "")),
            "timeRange": "",
            "status": state_map.get(str(row.get("schState") or ""), "公开排班"),
            "stopped": str(row.get("schState") or "") == "1",
            "price": str(row.get("regFee") or ""),
            "capacityHint": f"剩余 {num_remain} / 总量 {num_count}" if num_remain or num_count else "",
            "sourceType": "public_hospital_schedule_api_discovered",
            "sourceUrl": source_url,
            "dataLevel": "L1",
            "notes": "官网公开排班接口字段 numRemain/numCount，仅作为院方公开余号线索，不代表下单时实时可挂。",
            "confidence": "high",
        })
    return records


def discover_womanhospital_api(hospital: dict[str, str], timeout: int, max_records: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    base = "https://www.womanhospital.cn/flexoffice/api/w/his/duty/query"
    records: list[dict[str, Any]] = []
    api_pages: list[dict[str, Any]] = []
    area_url = f"{base}/getAreaList"
    area_payload, area_fetch = fetch_json(area_url, timeout)
    api_pages.append({
        "url": area_url,
        "linkText": "浙江妇保院区公开 API",
        "ok": area_fetch.ok,
        "status": area_fetch.status,
        "elapsedMs": area_fetch.elapsed_ms,
        "bytes": len(area_fetch.text),
        "scheduleSignal": False,
        "dateSignal": False,
        "error": area_fetch.error,
        "promotedRecords": 0,
        "parseSummary": {"api": "getAreaList", "areaCount": len((area_payload or {}).get("data") or [])},
    })
    for area in (area_payload or {}).get("data") or []:
        if len(records) >= max_records:
            break
        area_code = str(area.get("areaCode") or area.get("orgCode") or "")
        if not area_code:
            continue
        dept_url = f"{base}/getDeptTree?areaCode={urllib.parse.quote(area_code)}"
        dept_payload, dept_fetch = fetch_json(dept_url, timeout)
        depts = flatten_womanhospital_depts((dept_payload or {}).get("data") or [])
        api_pages.append({
            "url": dept_url,
            "linkText": f"浙江妇保{area_code}科室树公开 API",
            "ok": dept_fetch.ok,
            "status": dept_fetch.status,
            "elapsedMs": dept_fetch.elapsed_ms,
            "bytes": len(dept_fetch.text),
            "scheduleSignal": False,
            "dateSignal": False,
            "error": dept_fetch.error,
            "promotedRecords": 0,
            "parseSummary": {"api": "getDeptTree", "deptCount": len(depts)},
        })
        for dept in depts:
            if len(records) >= max_records:
                break
            params = urllib.parse.urlencode({
                "currentOrgCode": dept["orgCode"],
                "currentDeptId": dept["deptType"],
                "currentDeptTypeName": dept["deptTypeName"],
                "currentScheduleDate": "",
            })
            schedule_url = f"{base}/getDoctorScheduleList?{params}"
            schedule_payload, schedule_fetch = fetch_json(schedule_url, timeout)
            rows = (schedule_payload or {}).get("data") or []
            parsed = parse_womanhospital_schedule_rows(rows, hospital, schedule_url, max_records - len(records), len(records))
            records.extend(parsed)
            api_pages.append({
                "url": schedule_url,
                "linkText": f"浙江妇保{dept['deptTypeName']}排班公开 API",
                "ok": schedule_fetch.ok,
                "status": schedule_fetch.status,
                "elapsedMs": schedule_fetch.elapsed_ms,
                "bytes": len(schedule_fetch.text),
                "scheduleSignal": bool(rows),
                "dateSignal": any(row.get("schDate") for row in rows),
                "error": schedule_fetch.error,
                "promotedRecords": len(parsed),
                "parseSummary": {"api": "getDoctorScheduleList", "rawRowCount": len(rows)},
            })
    return records, api_pages


def extract_records_from_tables(hospital: dict[str, str], source_url: str, page_html: str, max_records: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    parser = TableParser()
    parser.feed(page_html)
    records: list[dict[str, Any]] = []
    table_summaries = []
    for table_index, rows in enumerate(parser.tables):
        if len(rows) < 2:
            continue
        caption = parser.captions[table_index] if table_index < len(parser.captions) else ""
        flat = " ".join([caption, *(" ".join(row) for row in rows)])
        score = sum(bool(regex.search(flat)) for regex in (SCHEDULE_PAGE_HINT, DATE_HINT, SLOT_HINT))
        date_columns = []
        for idx, cell in enumerate(rows[0]):
            if DATE_HINT.search(cell):
                iso_date, weekday = normalize_date(cell)
                date_columns.append({"index": idx, "raw": cell, "date": iso_date, "weekday": weekday})
        table_summaries.append({"tableIndex": table_index, "rowCount": len(rows), "score": score, "dateColumnCount": len(date_columns)})
        header = " ".join(rows[0])
        if score >= 2 and re.search(r"科室", header) and re.search(r"(专家|医生|医师)", header) and re.search(r"(时间|出诊)", header):
            current_department = ""
            for row_index, row in enumerate(rows[1:], start=1):
                if len(records) >= max_records:
                    break
                if len(row) < 2:
                    continue
                if len(row) >= 3:
                    department_cell, doctor_cell, time_cell = row[0], row[1], row[2]
                    if re.search(r"(科|中心|门诊|专病)", department_cell):
                        current_department = department_cell
                else:
                    department_cell, doctor_cell, time_cell = current_department, row[0], row[1]
                if not current_department and re.search(r"(科|中心|门诊|专病)", department_cell):
                    current_department = department_cell
                weekday = normalize_date(time_cell)[1]
                slot = SLOT_HINT.search(time_cell)
                if not current_department or not weekday or not slot or not looks_like_doctor_name(doctor_cell):
                    continue
                for doctor in split_doctors(doctor_cell):
                    records.append({
                        "id": f"{hospital['id']}-weekly-{len(records)}",
                        "city": hospital["city"],
                        "hospitalId": hospital["id"],
                        "hospitalName": hospital["name"],
                        "campusName": hospital.get("shortName") or hospital["name"],
                        "departmentName": current_department,
                        "standardDepartment": "",
                        "subDepartment": current_department,
                        "doctorName": doctor,
                        "doctorSpecial": "",
                        "professionalTitle": "",
                        "clinicLevel": "",
                        "visitDate": "",
                        "dateLabel": time_cell,
                        "weekday": weekday,
                        "displayDate": time_cell,
                        "timeSlot": slot.group(1),
                        "timeRange": "",
                        "status": "公开排班",
                        "stopped": "停诊" in time_cell,
                        "price": "",
                        "capacityHint": "",
                        "sourceType": "public_hospital_weekly_table",
                        "sourceUrl": source_url,
                        "dataLevel": "L1",
                        "notes": "官网周期出诊安排，不代表实时可挂",
                        "confidence": "high",
                    })
                    if len(records) >= max_records:
                        break
        if score < 2 or not date_columns:
            continue
        current_department = ""
        for row_index, row in enumerate(rows[1:], start=1):
            if len(records) >= max_records:
                break
            first_text = " ".join(row[:2])
            if re.search(r"(科|中心|门诊|专病)", first_text):
                current_department = row[0] or current_department
            slot = next((cell for cell in row[:3] if SLOT_HINT.search(cell)), "") or caption
            for column in date_columns:
                if column["index"] >= len(row):
                    continue
                cell = row[column["index"]]
                if not cell or re.fullmatch(r"[-—无/]+", cell):
                    continue
                if not looks_like_doctor_name(cell):
                    continue
                department = current_department or row[0] if row else ""
                doctors = split_doctors(cell)
                for doctor in doctors:
                    if SLOT_HINT.fullmatch(doctor) or SLOT_HINT.fullmatch(department):
                        continue
                    if len(records) >= max_records:
                        break
                    records.append({
                        "id": f"{hospital['id']}-auto-{len(records)}",
                        "city": hospital["city"],
                        "hospitalId": hospital["id"],
                        "hospitalName": hospital["name"],
                        "campusName": hospital.get("shortName") or hospital["name"],
                        "departmentName": department or "未标注科室",
                        "standardDepartment": "",
                        "subDepartment": department or "未标注科室",
                        "doctorName": doctor,
                        "doctorSpecial": "",
                        "professionalTitle": "",
                        "clinicLevel": "",
                        "visitDate": column["date"],
                        "dateLabel": column["raw"],
                        "weekday": column["weekday"],
                        "displayDate": " ".join(x for x in [column["date"], column["weekday"]] if x) or column["raw"],
                        "timeSlot": slot or "未标注",
                        "timeRange": "",
                        "status": "公开排班",
                        "stopped": "停诊" in cell,
                        "price": "",
                        "capacityHint": "",
                        "sourceType": "public_hospital_schedule_discovered",
                        "sourceUrl": source_url,
                        "dataLevel": "L1",
                        "notes": "自动发现的官网公开排班，已通过结构阈值；不代表实时可挂",
                        "confidence": "medium",
                    })
    return records, {"tableCount": len(parser.tables), "tableSummaries": table_summaries[:12]}


def discover_hospital(hospital: dict[str, str], timeout: int, max_pages: int, max_records: int, sleep: float) -> dict[str, Any]:
    official_site = hospital.get("officialSite", "")
    item: dict[str, Any] = {
        "city": hospital["city"],
        "hospitalId": hospital["id"],
        "hospitalName": hospital["name"],
        "officialSite": official_site,
        "homepage": {},
        "candidatePages": [],
        "promotedRecordCount": 0,
    }
    if hospital.get("officialSiteStatus") != "official" or not official_site:
        item["skipped"] = True
        item["skipReason"] = "source entry is not a verified hospital homepage"
        return item

    homepage = fetch(official_site, timeout)
    homepage_text = clean_text(homepage.text) if homepage.ok else ""
    item["homepage"] = {
        "ok": homepage.ok,
        "status": homepage.status,
        "elapsedMs": homepage.elapsed_ms,
        "bytes": len(homepage.text),
        "scheduleSignal": bool(SCHEDULE_PAGE_HINT.search(homepage_text)),
        "error": homepage.error,
    }
    if not homepage.ok:
        return item

    link_parser = LinkParser(official_site)
    link_parser.feed(homepage.text)
    urls: list[dict[str, str]] = []
    seen: set[str] = set()
    for link in link_parser.links:
        url = link["url"].split("#", 1)[0]
        if url in seen or not same_host_or_subpath(official_site, url):
            continue
        seen.add(url)
        urls.append({"url": url, "text": link["text"]})
    if not urls and item["homepage"]["scheduleSignal"]:
        urls.append({"url": official_site, "text": "homepage schedule signal"})

    all_records: list[dict[str, Any]] = []
    for link in urls[:max_pages]:
        time.sleep(sleep)
        page = fetch(link["url"], timeout)
        page_text = clean_text(page.text) if page.ok else ""
        page_item: dict[str, Any] = {
            "url": link["url"],
            "linkText": link["text"],
            "ok": page.ok,
            "status": page.status,
            "elapsedMs": page.elapsed_ms,
            "bytes": len(page.text),
            "scheduleSignal": bool(SCHEDULE_PAGE_HINT.search(page_text)),
            "dateSignal": bool(DATE_HINT.search(page_text)),
            "error": page.error,
            "promotedRecords": 0,
        }
        if page.ok:
            records, parse_summary = extract_records_from_tables(hospital, link["url"], page.text, max_records - len(all_records))
            page_item["parseSummary"] = parse_summary
            page_item["promotedRecords"] = len(records)
            all_records.extend(records)
        item["candidatePages"].append(page_item)
        if len(all_records) >= max_records:
            break
    if hospital["id"] == "hz_women" and len(all_records) < max_records:
        api_records, api_pages = discover_womanhospital_api(hospital, timeout, max_records - len(all_records))
        all_records.extend(api_records)
        item["candidatePages"].extend(api_pages)
    item["records"] = all_records
    item["promotedRecordCount"] = len(all_records)
    return item


def build_frontend_schedule_js(records_by_city: dict[str, list[dict[str, Any]]], report: dict[str, Any]) -> str:
    payload = {
        "generatedAt": report["generatedAt"],
        "source": "data-access-research/all_city_data_pipeline.py",
        "recordsByCity": records_by_city,
        "policy": "L1 public schedules only; not realtime availability.",
    }
    return "window.ALL_CITY_SCHEDULE_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n"


def total_record_count(records_by_city: dict[str, list[dict[str, Any]]]) -> int:
    return sum(len(records) for records in records_by_city.values())


def write_all_city_artifacts(
    records_by_city: dict[str, list[dict[str, Any]]],
    report: dict[str, Any],
    *,
    report_path: Path = REPORT_FILE,
    schedule_js_path: Path = SCHEDULE_JS_FILE,
) -> dict[str, Any]:
    """Write generated crawl artifacts only when the crawl found records.

    Empty crawls preserve the last known-good frontend data instead of replacing
    it with an empty payload.
    """
    total_records = total_record_count(records_by_city)
    if total_records == 0:
        return {
            "written": False,
            "reason": "empty_crawl",
            "totalRecordCount": 0,
            "reportPath": str(report_path),
            "scheduleJsPath": str(schedule_js_path),
        }

    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    schedule_js_path.write_text(build_frontend_schedule_js(records_by_city, report), encoding="utf-8")
    return {
        "written": True,
        "totalRecordCount": total_records,
        "reportPath": str(report_path),
        "scheduleJsPath": str(schedule_js_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover conservative all-city public schedule data.")
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--sleep", type=float, default=0.3)
    parser.add_argument("--max-pages-per-hospital", type=int, default=4)
    parser.add_argument("--max-records-per-hospital", type=int, default=120)
    parser.add_argument("--limit-per-city", type=int, default=0, help="Debug limit; 0 means all hospitals.")
    args = parser.parse_args()

    registries = parse_all_city_registries()
    discovered: list[dict[str, Any]] = []
    records_by_city: dict[str, list[dict[str, Any]]] = {city: [] for city in registries}
    for city, hospitals in registries.items():
        selected = hospitals[: args.limit_per_city] if args.limit_per_city else hospitals
        print(f"[pipeline] {city}: discovering {len(selected)} hospitals", flush=True)
        for hospital in selected:
            item = discover_hospital(hospital, args.timeout, args.max_pages_per_hospital, args.max_records_per_hospital, args.sleep)
            records = item.pop("records", [])
            records_by_city[city].extend(records)
            discovered.append(item)
            print(f"[pipeline] {city} {hospital['id']}: {len(records)} L1 records", flush=True)
            time.sleep(args.sleep)

    generated_at = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    report = {
        "generatedAt": generated_at,
        "policy": "Public official pages only; no login, CAPTCHA bypass, order flow, or personal-data collection.",
        "citySummary": {
            city: {
                "hospitalCount": len(registries[city][: args.limit_per_city] if args.limit_per_city else registries[city]),
                "promotedRecordCount": len(records),
                "hospitalsWithPromotedRecords": len({record["hospitalId"] for record in records}),
            }
            for city, records in records_by_city.items()
        },
        "discovered": discovered,
        "endToEndChecks": {},
    }
    artifact_result = write_all_city_artifacts(records_by_city, report)
    if not artifact_result["written"]:
        print("[pipeline] no L1 records discovered; preserving existing frontend schedule data", flush=True)
        print(f"[pipeline] skipped writing {REPORT_FILE}", flush=True)
        print(f"[pipeline] skipped writing {SCHEDULE_JS_FILE}", flush=True)
        return 1

    print(f"[pipeline] wrote {REPORT_FILE}", flush=True)
    print(f"[pipeline] wrote {SCHEDULE_JS_FILE}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
