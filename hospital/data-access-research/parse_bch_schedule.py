#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup


LEVEL_MAP = {
    "1": "普通门诊",
    "2": "专家门诊",
    "3": "特需门诊",
    "4": "知名门诊",
    "6": "专病门诊",
    "7": "知名专家团队",
    "8": "国际医疗部出诊",
}

PROFESSIONAL_MAP = {
    "1": "主任医师",
    "2": "副主任医师",
    "3": "主治医师",
    "4": "住院医师",
    "17": "知名专家",
}

STATE_MAP = {
    "0": "未开启预约",
    "2": "时间未到",
    "4": "可预约",
    "6": "时间已过",
    "8": "暂停",
    "10": "假期",
    "12": "约满",
    "14": "停诊",
    "16": "替诊",
    "18": "被替诊",
    "20": "换诊",
}


def text_of(node):
    return " ".join(node.get_text(" ", strip=True).split()) if node else ""


def icon_code(class_names, prefix):
    for class_name in class_names:
        if class_name.startswith(prefix):
            return class_name.removeprefix(prefix)
    return None


def parse_doctor_block(block):
    doctor_link = block.find("a")
    level_span = block.find("span", class_=re.compile(r"SchedulingLevel_icon\d+"))
    professional_span = block.find("span", class_=re.compile(r"SchedulingProfessional_icon\d+"))
    state_span = block.find("span", class_=re.compile(r"SchedulingState_icon\d+"))

    level_code = icon_code(level_span.get("class", []), "SchedulingLevel_icon") if level_span else None
    professional_code = icon_code(professional_span.get("class", []), "SchedulingProfessional_icon") if professional_span else None
    state_code = icon_code(state_span.get("class", []), "SchedulingState_icon") if state_span else None

    return {
        "doctorName": text_of(doctor_link),
        "doctorUrl": doctor_link.get("href") if doctor_link else None,
        "clinicLevel": LEVEL_MAP.get(level_code, level_code),
        "professionalTitle": PROFESSIONAL_MAP.get(professional_code, professional_code),
        "appointmentState": STATE_MAP.get(state_code, state_span.get("title") if state_span else "未标注"),
    }


def parse_schedule(html):
    soup = BeautifulSoup(html, "html.parser")

    title_text = text_of(soup.select_one("#Scheduling_title .Scheduling_time"))
    range_match = re.search(r"(\d{4}年\d{2}月\d{2}日)--(\d{4}年\d{2}月\d{2}日)", title_text)

    table = soup.select_one("#conTable_tableb_1 table#Scheduling_table")
    if not table:
        raise RuntimeError("Unable to find Beijing Children's Hospital schedule table")

    header_cells = table.select("tr.First_tr td")[2:]
    dates = [cell.get_text(" ", strip=True).replace(" ", "") for cell in header_cells]

    records = []
    current_department = None

    for row in table.select("tbody.searchDetail > tr"):
        cells = row.find_all("td", recursive=False)
        if not cells:
            continue

        idx = 0
        dep_cell = cells[0] if "depClass1" in cells[0].get("class", []) else None
        if dep_cell:
            dep_link = dep_cell.find("a")
            current_department = {
                "departmentName": text_of(dep_link),
                "departmentUrl": dep_link.get("href") if dep_link else None,
            }
            idx = 1

        if current_department is None or idx >= len(cells):
            continue

        slot = text_of(cells[idx]) or "其他"
        day_cells = cells[idx + 1: idx + 1 + len(dates)]

        for day, cell in zip(dates, day_cells):
            for block in cell.select(".showson"):
                parsed = parse_doctor_block(block)
                if not parsed["doctorName"]:
                    continue
                records.append({
                    "hospitalName": "首都医科大学附属北京儿童医院",
                    "sourceType": "public_hospital_schedule_page",
                    "sourceUrl": "http://www.bch.com.cn/Html/Hospitals/Schedulings/OPIndex0_0.html",
                    "scheduleRange": {
                        "raw": title_text,
                        "start": range_match.group(1) if range_match else None,
                        "end": range_match.group(2) if range_match else None,
                    },
                    "dateLabel": day,
                    "timeSlot": slot,
                    **current_department,
                    **parsed,
                })

    return records


def main():
    if len(sys.argv) != 3:
        print("Usage: parse_bch_schedule.py <input_html> <output_json>", file=sys.stderr)
        return 2

    html_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    records = parse_schedule(html_path.read_text(encoding="utf-8", errors="ignore"))
    output_path.write_text(json.dumps({
        "recordCount": len(records),
        "records": records,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(records)} records to {output_path}")


if __name__ == "__main__":
    raise SystemExit(main())
