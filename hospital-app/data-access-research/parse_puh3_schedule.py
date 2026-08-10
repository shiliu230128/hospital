#!/usr/bin/env python3
import json
import sys
from pathlib import Path


WEEKDAY_KEY_MAP = {
    "mondayData": "星期一",
    "tuesdayData": "星期二",
    "wednesdayData": "星期三",
    "thursdayData": "星期四",
    "fridayData": "星期五",
    "saturdayData": "星期六",
    "sundayData": "星期日",
}


def normalize_schedule(payload, source_url):
    records = []

    for clinic_row in payload.get("pageResult", {}).get("dataList", []):
        schedules = clinic_row.get("schedules") or {}
        for weekday_key, time_section_map in schedules.items():
            if not time_section_map:
                continue
            weekday = WEEKDAY_KEY_MAP.get(weekday_key, weekday_key)
            for _, items in time_section_map.items():
                for item in items or []:
                    stop_flag = str(item.get("stopFlag", ""))
                    records.append({
                        "hospitalName": "北京大学第三医院",
                        "campusName": item.get("hosAreaName"),
                        "campusId": item.get("hosAreaId"),
                        "sourceType": "public_hospital_schedule_api",
                        "sourceUrl": source_url,
                        "departmentName": item.get("clinicName") or clinic_row.get("clinicName"),
                        "departmentId": item.get("clinicId") or clinic_row.get("clinicId"),
                        "weekday": weekday,
                        "visitDate": item.get("curDayTime"),
                        "visitDateLabel": item.get("curDayTimeDay"),
                        "timeSlot": item.get("timeSectionName"),
                        "doctorName": item.get("doctorName"),
                        "doctorId": item.get("doctorId"),
                        "doctorSpecial": item.get("doctorSpecial"),
                        "professionalTitle": ", ".join([x for x in (item.get("docJobTitleDicName") or []) if x]),
                        "clinicLevel": item.get("consTypeDicCodeName"),
                        "groupName": item.get("groupName"),
                        "appointmentState": "停诊" if stop_flag == "1" else "未停诊",
                        "stopFlag": item.get("stopFlag"),
                        "clinicLimitCountRaw": item.get("signalSum"),
                        "priceCnyRaw": item.get("chargePrice"),
                        "dataType": item.get("dataType"),
                        "scheduleSource": item.get("scheduleSource"),
                        "rawScheduleId": item.get("id"),
                        "notes": "clinicLimitCountRaw 来自院方公开排班接口字段 signalSum，按当前验证只能作为门诊限号/容量线索，不能等同于实时剩余号源。",
                    })

    records.sort(key=lambda x: (
        x.get("visitDate") or "",
        x.get("timeSlot") or "",
        x.get("departmentName") or "",
        x.get("doctorName") or "",
    ))
    return records


def main():
    if len(sys.argv) != 3:
        print("Usage: parse_puh3_schedule.py <input_schedule_json> <output_json>", file=sys.stderr)
        return 2

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    source_url = "https://www.puh3.net.cn/aop_web/industry/patient/static/userClinic/getClinicSchedules/{areaId}/{clinicName}/{clinicId}"
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    records = normalize_schedule(payload, source_url)
    output_path.write_text(json.dumps({
        "recordCount": len(records),
        "sourceNote": "北京大学第三医院官网公开出停诊信息接口样本。该样本为公开排班/停诊/门诊限号信息，不代表授权实时余号。",
        "records": records,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(records)} records to {output_path}")


if __name__ == "__main__":
    raise SystemExit(main())
