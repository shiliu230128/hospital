#!/usr/bin/env python3
"""Regression tests for the all-city schedule pipeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import all_city_data_pipeline as pipeline  # noqa: E402


def make_report() -> dict[str, object]:
    return {
        "generatedAt": "2026-08-09T16:52:15+0800",
        "policy": "Public official pages only; no login, CAPTCHA bypass, order flow, or personal-data collection.",
        "citySummary": {
            "北京": {"hospitalCount": 1, "promotedRecordCount": 1, "hospitalsWithPromotedRecords": 1},
            "上海": {"hospitalCount": 0, "promotedRecordCount": 0, "hospitalsWithPromotedRecords": 0},
            "深圳": {"hospitalCount": 0, "promotedRecordCount": 0, "hospitalsWithPromotedRecords": 0},
            "杭州": {"hospitalCount": 0, "promotedRecordCount": 0, "hospitalsWithPromotedRecords": 0},
        },
        "discovered": [],
        "endToEndChecks": {},
    }


def test_skip_write_on_empty_crawl() -> int:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        frontend_dir = root / "frontend-prototype"
        data_dir = root / "data-access-research"
        frontend_dir.mkdir()
        data_dir.mkdir()
        report_path = data_dir / "all-city-crawl-report.json"
        schedule_path = frontend_dir / "all-city-schedule-data.js"
        report_path.write_text("REPORT-SENTINEL", encoding="utf-8")
        schedule_path.write_text("SCHEDULE-SENTINEL", encoding="utf-8")

        result = pipeline.write_all_city_artifacts(
            {"北京": [], "上海": [], "深圳": [], "杭州": []},
            make_report(),
            report_path=report_path,
            schedule_js_path=schedule_path,
        )

        if result.get("written") is not False:
            print(f"[FAIL] expected skipped write, got {result}")
            return 1
        if report_path.read_text(encoding="utf-8") != "REPORT-SENTINEL":
            print("[FAIL] empty crawl should not overwrite crawl report")
            return 1
        if schedule_path.read_text(encoding="utf-8") != "SCHEDULE-SENTINEL":
            print("[FAIL] empty crawl should not overwrite schedule data")
            return 1

        print("[PASS] empty crawl preserves existing artifacts")
        return 0


def test_write_on_nonempty_crawl() -> int:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        frontend_dir = root / "frontend-prototype"
        data_dir = root / "data-access-research"
        frontend_dir.mkdir()
        data_dir.mkdir()
        report_path = data_dir / "all-city-crawl-report.json"
        schedule_path = frontend_dir / "all-city-schedule-data.js"
        report_path.write_text("REPORT-SENTINEL", encoding="utf-8")
        schedule_path.write_text("SCHEDULE-SENTINEL", encoding="utf-8")

        record = {
            "id": "bj_friendship-auto-0",
            "city": "北京",
            "hospitalId": "bj_friendship",
            "hospitalName": "首都医科大学附属北京友谊医院",
            "campusName": "北京友谊医院",
            "departmentName": "消化中心",
            "standardDepartment": "",
            "subDepartment": "消化中心",
            "doctorName": "吕富靖",
            "doctorSpecial": "",
            "professionalTitle": "",
            "clinicLevel": "",
            "visitDate": "",
            "dateLabel": "星期一",
            "weekday": "星期一",
            "displayDate": "星期一",
            "timeSlot": "上午",
            "timeRange": "",
            "status": "公开排班",
            "stopped": False,
            "price": "",
            "capacityHint": "",
            "sourceType": "public_hospital_schedule_discovered",
            "sourceUrl": "https://www.bfh.com.cn/Html/Hospitals/Schedulings/OPIndex0_0.html",
            "dataLevel": "L1",
            "notes": "自动发现的官网公开排班，已通过结构阈值；不代表实时可挂",
            "confidence": "medium",
        }

        result = pipeline.write_all_city_artifacts(
            {"北京": [record], "上海": [], "深圳": [], "杭州": []},
            make_report(),
            report_path=report_path,
            schedule_js_path=schedule_path,
        )

        if result.get("written") is not True:
            print(f"[FAIL] expected write, got {result}")
            return 1
        if "REPORT-SENTINEL" in report_path.read_text(encoding="utf-8"):
            print("[FAIL] non-empty crawl should overwrite crawl report")
            return 1
        schedule_text = schedule_path.read_text(encoding="utf-8")
        if "SCHEDULE-SENTINEL" in schedule_text or "bj_friendship" not in schedule_text:
            print("[FAIL] non-empty crawl should overwrite schedule data")
            return 1

        print("[PASS] non-empty crawl writes refreshed artifacts")
        return 0


def main() -> int:
    errors = 0
    for name, func in (
        ("Skip write on empty crawl", test_skip_write_on_empty_crawl),
        ("Write on non-empty crawl", test_write_on_nonempty_crawl),
    ):
        print(f"\n--- {name} ---")
        try:
            errors += func()
        except Exception as exc:  # noqa: BLE001
            print(f"[ERROR] {name} raised: {exc}")
            errors += 1
    print(f"\n{'='*40}")
    if errors == 0:
        print("All tests passed.")
        return 0
    print(f"{errors} test failures.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
