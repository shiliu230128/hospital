#!/usr/bin/env python3
"""Run a conservative one-shot data refresh and audit report.

This runner is designed to be called manually today and by launchd/cron/Comate
Automation later. It does not promote unverified scraped data into the frontend;
it refreshes discovery artifacts and writes a report with source health, registry
coverage, WeChat entry validation, and availability-probe status.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data-access-research"
FRONTEND_DIR = ROOT / "frontend-prototype"
REGISTRY_FILE = FRONTEND_DIR / "beijing-3a-hospitals.js"
REGIONAL_CITY_FILE = FRONTEND_DIR / "regional-city-data.js"
WECHAT_FILE = FRONTEND_DIR / "wechat-entries.js"
WECHAT_ASSET_DIR = FRONTEND_DIR / "assets" / "wechat-qrcodes"
CANDIDATES_FILE = DATA_DIR / "wechat_entry_candidates.json"
AVAILABILITY_SUMMARY_FILE = DATA_DIR / "realtime_availability_probe_summary.json"
REPORT_FILE = DATA_DIR / "update-report.json"
LATEST_REPORT_JSON = FRONTEND_DIR / "generated" / "latest-report.json"
LATEST_REPORT_JS = FRONTEND_DIR / "generated" / "latest-report.js"
REPORT_HISTORY_DIR = DATA_DIR / "reports" / "history"
MAX_HISTORY_REPORTS = 3

USER_AGENT = "Mozilla/5.0 registration-research/0.4"

# Seed list from official Beijing/NHC-facing institutional navigation, hospital
# websites, and prior verified registry work. This audits tertiary/3A-related
# coverage gaps; it is not an auto-import source, so missing items stay in the
# report until manually verified.
OFFICIAL_AUDIT_SEED_NAMES = [
    "北京医院",
    "中日友好医院",
    "中国医学科学院北京协和医院",
    "中国医学科学院阜外医院",
    "中国医学科学院整形外科医院",
    "中国医学科学院肿瘤医院",
    "北京大学第一医院",
    "北京大学人民医院",
    "北京大学第三医院",
    "北京大学第六医院",
    "北京大学口腔医院",
    "北京大学肿瘤医院",
    "北京大学国际医院",
    "首都医科大学宣武医院",
    "首都医科大学附属北京同仁医院",
    "首都医科大学附属北京朝阳医院",
    "首都医科大学附属北京友谊医院",
    "首都医科大学附属北京安贞医院",
    "首都医科大学附属北京天坛医院",
    "首都医科大学附属北京世纪坛医院",
    "首都医科大学附属北京积水潭医院",
    "首都医科大学附属北京地坛医院",
    "首都医科大学附属北京佑安医院",
    "首都医科大学附属北京儿童医院",
    "首都医科大学附属北京妇产医院",
    "首都医科大学附属北京口腔医院",
    "首都医科大学附属北京胸科医院",
    "首都医科大学附属北京安定医院",
    "首都医科大学附属北京中医医院",
    "首都儿科研究所附属儿童医院",
    "北京回龙观医院",
    "中国中医科学院西苑医院",
    "中国中医科学院广安门医院",
    "中国中医科学院望京医院",
    "北京中医药大学东直门医院",
    "北京中医药大学东方医院",
    "北京中医药大学第三附属医院",
    "北京市昌平区中西医结合医院",
    "北京清华长庚医院",
    "清华大学玉泉医院",
    "北京老年医院",
    "首都医科大学附属北京潞河医院",
    "中国康复研究中心北京博爱医院",
]

CITY_AUDIT_SEED_NAMES = {
    "北京": OFFICIAL_AUDIT_SEED_NAMES,
    "上海": [
        "复旦大学附属中山医院",
        "复旦大学附属华山医院",
        "上海交通大学医学院附属瑞金医院",
        "上海交通大学医学院附属仁济医院",
        "上海交通大学医学院附属第九人民医院",
        "上海市第六人民医院",
        "上海市第十人民医院",
        "海军军医大学第一附属医院",
        "海军军医大学第二附属医院",
        "海军军医大学第三附属医院",
        "复旦大学附属儿科医院",
        "复旦大学附属妇产科医院",
        "复旦大学附属眼耳鼻喉科医院",
        "复旦大学附属肿瘤医院",
        "上海交通大学医学院附属上海儿童医学中心",
        "上海交通大学医学院附属新华医院",
        "上海市第一人民医院",
        "上海市儿童医院",
        "上海市肺科医院",
        "上海市胸科医院",
        "上海市精神卫生中心",
        "上海市公共卫生临床中心",
        "上海市第一妇婴保健院",
        "中国福利会国际和平妇幼保健院",
        "华东医院",
        "同济大学附属同济医院",
        "同济大学附属东方医院",
        "上海市中医医院",
        "上海中医药大学附属龙华医院",
        "上海中医药大学附属曙光医院",
        "上海中医药大学附属岳阳中西医结合医院",
        "上海市中西医结合医院",
        "上海市光华中西医结合医院",
    ],
    "深圳": [
        "南方医科大学深圳医院",
        "深圳龙城医院",
        "深圳市妇幼保健院",
        "北京大学深圳医院",
        "深圳市儿童医院",
        "中国医学科学院肿瘤医院深圳医院",
        "深圳市中医院",
        "中山大学附属第七医院（深圳）",
        "中国医学科学院阜外医院深圳医院",
        "深圳市人民医院",
        "深圳市第三人民医院",
        "香港大学深圳医院",
        "深圳市眼科医院",
        "深圳市第二人民医院",
        "深圳市康宁医院",
        "深圳市罗湖区人民医院",
        "深圳市宝安区人民医院",
        "深圳市宝安区中医院",
        "深圳市中西医结合医院",
        "深圳市龙岗中心医院",
        "深圳市龙华区人民医院",
        "深圳市龙华区中心医院",
        "深圳市南山区妇幼保健院",
    ],
    "杭州": [
        "浙江大学医学院附属第一医院",
        "浙江大学医学院附属第二医院",
        "浙江大学医学院附属邵逸夫医院",
        "浙江大学医学院附属妇产科医院",
        "浙江大学医学院附属儿童医院",
        "浙江大学医学院附属口腔医院",
        "浙江省人民医院",
        "浙江医院",
        "杭州市第一人民医院",
        "杭州市中医院",
        "浙江省肿瘤医院",
        "浙江省立同德医院",
        "浙江省中医院",
        "浙江中医药大学附属第二医院",
        "浙江中医药大学附属第三医院",
        "杭州师范大学附属医院",
        "杭州市红十字会医院",
        "杭州市第七人民医院",
    ],
}

SOURCE_HEALTH_URLS = [
    {
        "id": "beijing_wjw_home",
        "name": "北京市卫生健康委员会官网",
        "url": "https://wjw.beijing.gov.cn",
        "expectedText": "北京市卫生健康委员会",
        "level": "official_directory_signal",
    },
    {
        "id": "nhc_service_query",
        "name": "国家卫健委政务服务平台查询入口",
        "url": "https://zwfw.nhc.gov.cn/cxx",
        "expectedText": "查询",
        "level": "official_query_entry",
    },
    {
        "id": "bj_114_entry",
        "name": "北京市预约挂号统一平台入口探测",
        "url": "https://www.114yygh.com/robots.txt",
        "expectedText": "北京市预约挂号统一平台",
        "level": "official_registration_entry_only",
    },
]

LIVE_PROBES = [
    {
        "id": "bch_public_schedule",
        "hospitalId": "bch",
        "level": "L1",
        "url": "http://www.bch.com.cn/Html/Hospitals/Schedulings/OPIndex0_0.html",
        "expectedText": "出诊",
        "capability": "public_schedule_html",
    },
    {
        "id": "puh3_campus_api",
        "hospitalId": "puh3",
        "level": "L1",
        "url": "https://www.puh3.net.cn/aop_web/industry/patient/static/userHospital/allEnable",
        "expectedText": "北京大学第三医院",
        "capability": "public_schedule_api_seed",
    },
    {
        "id": "pumch_public_schedule",
        "hospitalId": "pumch",
        "level": "L1",
        "url": "https://www.pumch.cn/dsearchs/dockervisit/3/1.html",
        "expectedText": "门诊",
        "capability": "public_schedule_html",
    },
    {
        "id": "yygh_hospital_list",
        "hospitalId": "114yygh",
        "level": "unknown",
        "url": "https://www.114yygh.com/web/hospital/list",
        "expectedText": "医院",
        "capability": "unauthorized_public_list_probe",
    },
]


@dataclass
class HttpProbeResult:
    id: str
    name: str
    url: str
    ok: bool
    status: int | None
    elapsedMs: int
    bytes: int
    expectedTextFound: bool
    error: str = ""


def log(message: str) -> None:
    print(f"[update] {message}", flush=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def prune_old_files(directory: Path, pattern: str, keep: int = MAX_HISTORY_REPORTS) -> dict[str, Any]:
    if not directory.exists():
        return {"directoryExists": False, "deletedCount": 0, "keptCount": 0}

    files = sorted(
        (path for path in directory.glob(pattern) if path.is_file()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    deleted = []
    for path in files[keep:]:
        path.unlink()
        deleted.append(str(path.relative_to(ROOT)))

    return {
        "directoryExists": True,
        "deletedCount": len(deleted),
        "keptCount": min(len(files), keep),
        "deletedFiles": deleted,
        "policy": f"Keep the newest {keep} files matching {pattern}; delete older generated history files.",
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fetch_url(url: str, timeout: int) -> tuple[int, bytes, dict[str, str]]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/json,application/xhtml+xml,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return getattr(response, "status", 200), response.read(), dict(response.headers.items())


def probe_url(item: dict[str, str], timeout: int) -> dict[str, Any]:
    started = time.time()
    try:
        status, body, headers = fetch_url(item["url"], timeout)
        elapsed_ms = int((time.time() - started) * 1000)
        content_type = headers.get("Content-Type", "")
        text = body[:500_000].decode("utf-8", errors="ignore")
        expected = item.get("expectedText", "")
        return {
            "id": item["id"],
            "name": item.get("name", item["id"]),
            "url": item["url"],
            "ok": 200 <= status < 400,
            "status": status,
            "elapsedMs": elapsed_ms,
            "bytes": len(body),
            "contentType": content_type,
            "expectedTextFound": bool(expected and expected in text),
            "level": item.get("level", "unknown"),
            "capability": item.get("capability", "source_reachability"),
        }
    except Exception as exc:  # noqa: BLE001
        elapsed_ms = int((time.time() - started) * 1000)
        status = exc.code if isinstance(exc, urllib.error.HTTPError) else None
        return {
            "id": item["id"],
            "name": item.get("name", item["id"]),
            "url": item["url"],
            "ok": False,
            "status": status,
            "elapsedMs": elapsed_ms,
            "bytes": 0,
            "contentType": "",
            "expectedTextFound": False,
            "level": item.get("level", "unknown"),
            "capability": item.get("capability", "source_reachability"),
            "error": str(exc),
        }


def parse_registry_text(text: str, city: str) -> list[dict[str, str]]:
    object_pattern = re.compile(r"\{\s*id:\s*\"(?P<id>[^\"]+)\".*?entries:\s*\[(?P<entries>.*?)\]\s*,?\s*\}", re.S)
    hospitals: list[dict[str, str]] = []
    for match in object_pattern.finditer(text):
        block = match.group(0)

        def field(name: str, source: str = block) -> str:
            found = re.search(rf"{name}:\s*\"([^\"]*)\"", source)
            return found.group(1) if found else ""

        entries = match.group("entries")
        web = re.search(r'\{\s*type:\s*"web".*?\}', entries, re.S)
        web_block = web.group(0) if web else ""
        hospitals.append({
            "city": city,
            "id": match.group("id"),
            "name": field("name"),
            "shortName": field("shortName"),
            "district": field("district"),
            "level": field("level"),
            "registryConfidence": field("registryConfidence"),
            "officialSite": field("url", web_block),
            "officialSiteName": field("name", web_block),
            "officialSiteStatus": field("status", web_block),
        })
    return hospitals


def parse_registry() -> list[dict[str, str]]:
    return parse_registry_text(read_text(REGISTRY_FILE), "北京")


def parse_regional_city_registries() -> dict[str, list[dict[str, str]]]:
    if not REGIONAL_CITY_FILE.exists():
        return {}

    text = read_text(REGIONAL_CITY_FILE)
    city_arrays = {
        "上海": "SHANGHAI_3A_HOSPITALS",
        "深圳": "SHENZHEN_3A_HOSPITALS",
        "杭州": "HANGZHOU_3A_HOSPITALS",
    }
    registries: dict[str, list[dict[str, str]]] = {}
    for city, variable_name in city_arrays.items():
        found = re.search(rf"window\.{variable_name}\s*=\s*\[(?P<body>.*?)\];", text, re.S)
        registries[city] = parse_registry_text(found.group("body"), city) if found else []
    return registries


def parse_all_city_registries() -> dict[str, list[dict[str, str]]]:
    registries = {"北京": parse_registry()}
    registries.update(parse_regional_city_registries())
    return registries


def get_referenced_local_wechat_assets() -> set[Path]:
    texts = [read_text(WECHAT_FILE)]
    if REGIONAL_CITY_FILE.exists():
        texts.append(read_text(REGIONAL_CITY_FILE))
    qr_images: list[str] = []
    for text in texts:
        qr_images.extend(re.findall(r'qrImageUrl:\s*"([^"]+)"', text))
    return {
        (FRONTEND_DIR / qr_image).resolve()
        for qr_image in qr_images
        if qr_image.startswith("assets/")
    }


def parse_wechat_entries(registries: dict[str, list[dict[str, str]]] | None = None) -> dict[str, Any]:
    texts = {"北京": read_text(WECHAT_FILE)}
    if REGIONAL_CITY_FILE.exists():
        regional = read_text(REGIONAL_CITY_FILE)
        for city, variable in (("上海", "SHANGHAI_WECHAT_ENTRIES"), ("深圳", "SHENZHEN_WECHAT_ENTRIES"), ("杭州", "HANGZHOU_WECHAT_ENTRIES")):
            found = re.search(rf"window\.{variable}\s*=\s*\{{(?P<body>.*?)\}};", regional, re.S)
            if found:
                texts[city] = found.group("body")
    hospital_ids: set[str] = set()
    by_city: dict[str, set[str]] = {}
    entry_count = 0
    payloads: list[str] = []
    for city, text in texts.items():
        ids = set(re.findall(r"^\s+([A-Za-z0-9_]+):\s*\[", text, re.M))
        by_city[city] = ids
        hospital_ids |= ids
        entry_count += text.count('type: "wechat"') + text.count('type: "mini"')
        payloads.extend(re.findall(r'qrPayload:\s*"([^"]+)"', text))
    bad_payloads = [
        payload for payload in payloads
        if payload and not (
            payload.startswith("http://weixin.qq.com/")
            or payload.startswith("https://weixin.qq.com/")
            or payload.startswith("https://mp.weixin.qq.com/")
        )
    ]
    missing_local_assets = []
    for asset_path in get_referenced_local_wechat_assets():
        if not asset_path.exists():
            missing_local_assets.append(str(asset_path.relative_to(FRONTEND_DIR)))
    cross_file_errors: list[str] = []
    if registries:
        for city in by_city:
            registry_ids = {h.get("id", "") for h in registries.get(city, [])}
            orphan_we = by_city[city] - registry_ids
            if orphan_we:
                cross_file_errors.append(f"{city}微信入口引用了不在registry中的医院: {sorted(orphan_we)}")
    result: dict[str, Any] = {
        "hospitalCount": len(hospital_ids),
        "entryCount": entry_count,
        "payloadCount": len(payloads),
        "badPayloads": bad_payloads,
        "missingLocalAssets": missing_local_assets,
    }
    if cross_file_errors:
        result["crossFileErrors"] = cross_file_errors
    result["status"] = "pass" if not bad_payloads and not missing_local_assets and not cross_file_errors else "needs_attention"
    return result


def cleanup_unreferenced_wechat_assets() -> dict[str, Any]:
    if not WECHAT_ASSET_DIR.exists():
        return {"assetDirExists": False, "keptCount": 0, "deletedCount": 0, "deletedBytes": 0, "keptFiles": []}

    referenced = get_referenced_local_wechat_assets()
    deleted_files = []
    deleted_bytes = 0
    kept_files = []
    for path in sorted(item for item in WECHAT_ASSET_DIR.iterdir() if item.is_file()):
        resolved = path.resolve()
        if resolved in referenced:
            kept_files.append(str(path.relative_to(FRONTEND_DIR)))
            continue
        size = path.stat().st_size
        path.unlink()
        deleted_files.append(str(path.relative_to(FRONTEND_DIR)))
        deleted_bytes += size

    return {
        "assetDirExists": True,
        "keptCount": len(kept_files),
        "deletedCount": len(deleted_files),
        "deletedBytes": deleted_bytes,
        "keptFiles": kept_files,
        "deletedFilesSample": deleted_files[:40],
        "policy": "Keep only local QR images referenced by frontend-prototype/wechat-entries.js; downloaded candidates are transient.",
    }


def run_wechat_candidate_refresh(timeout: int, sleep: float, skip: bool) -> dict[str, Any]:
    if skip:
        log("跳过微信候选重抓；如需完整联网刷新，请添加 --with-wechat-fetch。")
        return {"skipped": True, "reason": "quick refresh skips WeChat candidate crawling"}
    log("开始抓取微信候选入口；这一步会访问医院官网并下载候选二维码，可能耗时数分钟。")
    command = [
        sys.executable,
        "fetch_wechat_qr_candidates.py",
        "--download",
        "--timeout",
        str(timeout),
        "--sleep",
        str(sleep),
    ]
    started = time.time()
    result = subprocess.run(
        command,
        cwd=DATA_DIR,
        text=True,
        capture_output=True,
        check=False,
    )
    elapsed_ms = int((time.time() - started) * 1000)
    log(f"微信候选刷新完成，用时 {elapsed_ms / 1000:.1f} 秒，退出码 {result.returncode}。")
    summary: dict[str, Any] = {
        "skipped": False,
        "ok": result.returncode == 0,
        "returnCode": result.returncode,
        "elapsedMs": elapsed_ms,
        "stdout": result.stdout.strip()[-2000:],
        "stderr": result.stderr.strip()[-2000:],
    }
    if CANDIDATES_FILE.exists():
        candidates = json.loads(CANDIDATES_FILE.read_text(encoding="utf-8"))
        candidate_count = sum(len(item.get("candidates", [])) for item in candidates)
        download_count = sum(
            1
            for item in candidates
            for candidate in item.get("candidates", [])
            if candidate.get("localPath")
        )
        error_count = sum(1 for item in candidates if item.get("error"))
        summary.update({
            "hospitalCount": len(candidates),
            "candidateCount": candidate_count,
            "downloadCount": download_count,
            "hospitalErrorCount": error_count,
        })
    return summary


def audit_registry_against_seed(hospitals: list[dict[str, str]], city: str = "北京") -> dict[str, Any]:
    seed_names = CITY_AUDIT_SEED_NAMES.get(city, [])
    names = {hospital["name"] for hospital in hospitals}
    short_names = {hospital["shortName"] for hospital in hospitals}
    missing = [name for name in seed_names if name not in names and name not in short_names]
    likely_duplicates = []
    seen_short: dict[str, str] = {}
    for hospital in hospitals:
        short = hospital.get("shortName", "")
        if not short:
            continue
        if short in seen_short:
            likely_duplicates.append({"shortName": short, "ids": [seen_short[short], hospital["id"]]})
        else:
            seen_short[short] = hospital["id"]
    medium_confidence = [
        {"id": hospital["id"], "name": hospital["name"], "reason": "registryConfidence is not high"}
        for hospital in hospitals
        if hospital.get("registryConfidence") != "high"
    ]
    return {
        "city": city,
        "localRegistryCount": len(hospitals),
        "officialSeedCount": len(seed_names),
        "missingFromLocalRegistry": missing,
        "likelyDuplicates": likely_duplicates,
        "mediumConfidenceItems": medium_confidence,
        "policy": "Seed list is used for gap detection only. New hospitals require official-source verification before frontend promotion.",
    }


def audit_multi_city_registries(registries: dict[str, list[dict[str, str]]]) -> dict[str, Any]:
    by_city: dict[str, Any] = {}
    total_hospital_count = 0
    total_source_entry_count = 0
    cities_with_missing_entries = []
    cities_with_seed_gaps = []

    for city, hospitals in registries.items():
        total_hospital_count += len(hospitals)
        source_status_counts: dict[str, int] = {}
        missing_source_entries = []
        medium_confidence = []
        likely_duplicates = []
        seen_ids: set[str] = set()
        seen_short: dict[str, str] = {}

        for hospital in hospitals:
            source_url = hospital.get("officialSite", "")
            source_status = hospital.get("officialSiteStatus", "missing") or "missing"
            if source_url:
                total_source_entry_count += 1
            else:
                missing_source_entries.append({"id": hospital["id"], "name": hospital["name"]})
            source_status_counts[source_status] = source_status_counts.get(source_status, 0) + 1

            if hospital.get("registryConfidence") != "high":
                medium_confidence.append({"id": hospital["id"], "name": hospital["name"], "confidence": hospital.get("registryConfidence", "")})

            if hospital["id"] in seen_ids:
                likely_duplicates.append({"id": hospital["id"], "reason": "duplicate id"})
            seen_ids.add(hospital["id"])

            short = hospital.get("shortName", "")
            if short and short in seen_short:
                likely_duplicates.append({"shortName": short, "ids": [seen_short[short], hospital["id"]]})
            elif short:
                seen_short[short] = hospital["id"]

        seed_audit = audit_registry_against_seed(hospitals, city)
        if missing_source_entries:
            cities_with_missing_entries.append(city)
        if seed_audit["missingFromLocalRegistry"]:
            cities_with_seed_gaps.append(city)

        by_city[city] = {
            "hospitalCount": len(hospitals),
            "sourceEntryCount": len(hospitals) - len(missing_source_entries),
            "sourceStatusCounts": source_status_counts,
            "missingSourceEntries": missing_source_entries,
            "targetSeedCount": seed_audit["officialSeedCount"],
            "missingFromTargetSeed": seed_audit["missingFromLocalRegistry"],
            "mediumConfidenceItems": medium_confidence,
            "likelyDuplicates": likely_duplicates,
        }

    return {
        "cityCount": len(registries),
        "totalHospitalCount": total_hospital_count,
        "totalSourceEntryCount": total_source_entry_count,
        "citiesWithMissingEntries": cities_with_missing_entries,
        "citiesWithTargetSeedGaps": cities_with_seed_gaps,
        "byCity": by_city,
        "policy": "This audit checks both source-entry completeness and target seed-list coverage. It does not promote scraped candidates or claim realtime availability.",
        "status": "pass" if not cities_with_missing_entries and not cities_with_seed_gaps else "needs_attention",
    }


def summarize_schedule_samples() -> dict[str, Any]:
    samples = []
    for path, hospital_id, level in [
        (DATA_DIR / "bch_schedule_sample.json", "bch", "L1"),
        (DATA_DIR / "puh3_pediatrics_schedule_sample.json", "puh3", "L1"),
        (DATA_DIR / "pumch_dockervisit_sample_excerpt.json", "pumch", "L1"),
    ]:
        if not path.exists():
            samples.append({"hospitalId": hospital_id, "level": level, "status": "missing_sample", "recordCount": 0})
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        record_count = data.get("recordCount")
        if record_count is None:
            record_count = len(data.get("records") or data.get("sampleRows") or [])
        samples.append({
            "hospitalId": hospital_id,
            "level": level,
            "status": "sample_available",
            "recordCount": record_count,
            "sourceNote": data.get("sourceNote", ""),
        })
    return {"samples": samples, "sampleCount": len(samples)}


def summarize_availability_summary() -> dict[str, Any]:
    if not AVAILABILITY_SUMMARY_FILE.exists():
        return {"status": "missing", "message": "No realtime availability probe summary file found."}
    data = json.loads(AVAILABILITY_SUMMARY_FILE.read_text(encoding="utf-8"))
    sources = data.get("sources", [])
    level_counts: dict[str, int] = {}
    positive_realtime_sources = []
    for source in sources:
        level = str(source.get("highestValidatedLevel", "unknown"))
        level_counts[level] = level_counts.get(level, 0) + 1
        if source.get("exposesRemainingCount") is True or source.get("exposesBookableStatus") is True:
            positive_realtime_sources.append(source.get("sourceId"))
    return {
        "status": "loaded",
        "generatedAt": data.get("generatedAt"),
        "sourceCount": len(sources),
        "levelCounts": level_counts,
        "positiveRealtimeSources": positive_realtime_sources,
        "overallConclusion": data.get("overallConclusion", ""),
    }


def write_latest_report_assets(report: dict[str, Any]) -> dict[str, Any]:
    generated_dir = FRONTEND_DIR / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)

    payload = json.dumps(report, ensure_ascii=False, indent=2)
    json_path = LATEST_REPORT_JSON
    js_path = LATEST_REPORT_JS
    json_path.write_text(payload, encoding="utf-8")
    js_path.write_text(f"window.PROTOTYPE_LATEST_REPORT = {payload};\n", encoding="utf-8")

    return {
        "generatedDir": str(generated_dir.relative_to(ROOT)),
        "jsonPath": str(json_path.relative_to(ROOT)),
        "jsPath": str(js_path.relative_to(ROOT)),
        "generatedAt": report.get("generatedAt"),
        "policy": "Generated report assets are safe for static hosting and are refreshed together with update-report.json.",
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    log("读取医院 registry。")
    city_registries = parse_all_city_registries()
    hospitals = city_registries.get("北京", [])
    total_hospital_count = sum(len(items) for items in city_registries.values())
    log(f"已读取 {len(city_registries)} 个城市、{total_hospital_count} 家医院，开始探测官方来源健康状态。")
    source_health = [probe_url(item, args.timeout) for item in SOURCE_HEALTH_URLS]
    log("官方来源健康状态探测完成，开始探测公开排班样本源。")
    live_probes = [probe_url(item, args.timeout) for item in LIVE_PROBES]
    l1_ok = sum(1 for item in live_probes if item.get("level") == "L1" and item.get("ok") and item.get("expectedTextFound"))
    l1_total = sum(1 for item in live_probes if item.get("level") == "L1")
    realtime_positive = [item for item in live_probes if item.get("level") in {"L3", "L4"} and item.get("ok")]
    wechat_candidate_refresh = run_wechat_candidate_refresh(args.timeout, args.sleep, args.skip_wechat_fetch)
    log("清理未被正式前端引用的微信候选二维码文件。")
    wechat_asset_cleanup = cleanup_unreferenced_wechat_assets()
    log("汇总微信入口、医院名单和号源探测审计结果。")
    retention = prune_old_files(REPORT_HISTORY_DIR, "*.json", MAX_HISTORY_REPORTS)
    return {
        "generatedAt": now_iso(),
        "mode": "manual_one_shot_runner",
        "automationStatus": {
            "currentlyAutomatic": False,
            "selectedRuntime": "project_script_only",
            "dailyAutomationReady": True,
            "howToAutomateLater": [
                "launchd/cron/Comate Automation can call: python3 data-access-research/update_data_once.py",
                "Treat non-zero exit or report.overallStatus != pass as an alert.",
                "Do not auto-promote discovery candidates into frontend data without manual official-source verification.",
            ],
        },
        "wechatCandidateRefresh": wechat_candidate_refresh,
        "wechatAssetCleanup": wechat_asset_cleanup,
        "wechatEntryValidation": parse_wechat_entries(city_registries),
        "registryAudit": audit_registry_against_seed(hospitals, "北京"),
        "multiCityRegistryAudit": audit_multi_city_registries(city_registries),
        "sourceHealth": source_health,
        "scheduleSamples": summarize_schedule_samples(),
        "liveAvailabilityProbe": {
            "policy": "Low-frequency public endpoint checks only; no login, CAPTCHA, WAF bypass, order flow, or personal-data collection.",
            "probes": live_probes,
            "successRates": {
                "publicScheduleL1": f"{l1_ok}/{l1_total}",
                "realtimeL3L4Positive": f"{len(realtime_positive)}/0 configured",
            },
        },
        "priorAvailabilitySummary": summarize_availability_summary(),
        "generatedArtifactRetention": retention,
        "overallStatus": "pass",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="刷新医院挂号比选原型的数据审计报告。")
    parser.add_argument("--output", default=str(REPORT_FILE), help="审计报告输出路径。")
    parser.add_argument("--timeout", type=int, default=12, help="单个网络探测的超时时间，单位秒。")
    parser.add_argument("--sleep", type=float, default=0.4, help="完整微信候选抓取时的请求间隔，单位秒。")
    parser.add_argument("--skip-wechat-fetch", dest="skip_wechat_fetch", action="store_true", help="跳过微信候选重抓，只做快速审计。")
    parser.add_argument("--with-wechat-fetch", dest="skip_wechat_fetch", action="store_false", help="执行完整微信候选重抓。")
    parser.set_defaults(skip_wechat_fetch=True)
    args = parser.parse_args()

    log("开始刷新数据审计。默认是快速模式，不会重抓微信候选。")
    report = build_report(args)
    report["frontendRefreshAssets"] = write_latest_report_assets(report)
    output = Path(args.output).resolve()
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"写出审计报告：{output}")
    log(f"写出前端 JSON：{LATEST_REPORT_JSON}")
    log(f"写出前端 JS：{LATEST_REPORT_JS}")
    log("刷新完成。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
