#!/usr/bin/env python3
"""Validate generated all-city frontend data and append checks to the crawl report."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT / "frontend-prototype"
DATA_DIR = ROOT / "data-access-research"
SCHEDULE_JS = FRONTEND_DIR / "all-city-schedule-data.js"
REPORT = DATA_DIR / "all-city-crawl-report.json"
UPDATE_REPORT = DATA_DIR / "update-report.json"
PROTOTYPE_DATA_JS = FRONTEND_DIR / "prototype-data.js"
WECHAT_FILES = [FRONTEND_DIR / "wechat-entries.js", FRONTEND_DIR / "regional-city-data.js"]


def parse_window_assignment(path: Path, variable: str) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"window\.{re.escape(variable)}\s*=\s*(\{{.*\}});\s*$", text, re.S)
    if not match:
        raise RuntimeError(f"Unable to parse {variable} from {path}")
    return json.loads(match.group(1))


def validate_records(payload: dict[str, Any]) -> dict[str, Any]:
    required = {"hospitalId", "hospitalName", "departmentName", "doctorName", "sourceUrl", "dataLevel"}
    bad_terms = re.compile(r"^(上午|下午|晚上|夜间|全天|停诊|约满|门诊|专家|普通|专科|星期[一二三四五六日]|周[一二三四五六日])$")
    city_checks = {}
    total_records = 0
    for city, records in payload.get("recordsByCity", {}).items():
        total_records += len(records)
        missing_required = [record for record in records if any(not record.get(key) for key in required)]
        bad_doctors = [record for record in records if bad_terms.fullmatch(str(record.get("doctorName", "")))]
        non_l1 = [record for record in records if record.get("dataLevel") != "L1"]
        city_checks[city] = {
            "recordCount": len(records),
            "hospitalCount": len({record.get("hospitalId") for record in records}),
            "missingRequiredCount": len(missing_required),
            "badDoctorTokenCount": len(bad_doctors),
            "nonL1Count": len(non_l1),
            "sample": records[:3],
        }
    has_records = total_records > 0
    structural_ok = all(
        item["missingRequiredCount"] == 0 and item["badDoctorTokenCount"] == 0 and item["nonL1Count"] == 0
        for item in city_checks.values()
    )
    return {
        "status": "pass" if structural_ok and has_records else "needs_attention",
        "totalRecordCount": total_records,
        "emptyCrawl": not has_records,
        "byCity": city_checks,
    }


def validate_wechat_assets() -> dict[str, Any]:
    local_paths = []
    remote_paths = []
    for path in WECHAT_FILES:
        text = path.read_text(encoding="utf-8")
        for qr_path in re.findall(r'qrImageUrl:\s*"([^"]+)"', text):
            if qr_path.startswith("assets/"):
                local_paths.append(qr_path)
            else:
                remote_paths.append(qr_path)
    missing = [qr_path for qr_path in local_paths if not (FRONTEND_DIR / qr_path).exists()]
    return {
        "status": "pass" if not missing else "needs_attention",
        "localReferenceCount": len(local_paths),
        "remoteReferenceCount": len(remote_paths),
        "missingLocalAssets": missing,
    }


def validate_prototype_data_freshness() -> dict[str, Any]:
    if not PROTOTYPE_DATA_JS.exists():
        return {
            "status": "needs_attention",
            "message": f"{PROTOTYPE_DATA_JS.name} not found.",
        }

    text = PROTOTYPE_DATA_JS.read_text(encoding="utf-8")
    match = re.search(r"window\.PROTOTYPE_RAW_DATA\s*=\s*(\{.*\});\s*$", text, re.S)
    if not match:
        return {
            "status": "needs_attention",
            "message": f"Unable to parse {PROTOTYPE_DATA_JS.name}.",
        }

    payload = json.loads(match.group(1))
    update_report = json.loads(UPDATE_REPORT.read_text(encoding="utf-8"))
    generated_at = payload.get("generatedAt")
    expected_at = update_report.get("generatedAt")
    return {
        "status": "pass" if generated_at == expected_at else "needs_attention",
        "generatedAt": generated_at,
        "expectedGeneratedAt": expected_at,
        "prototypeDataPath": str(PROTOTYPE_DATA_JS.relative_to(FRONTEND_DIR)),
    }


def main() -> int:
    payload = parse_window_assignment(SCHEDULE_JS, "ALL_CITY_SCHEDULE_DATA")
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    checks = {
        "scheduleData": validate_records(payload),
        "wechatAssets": validate_wechat_assets(),
        "prototypeDataFreshness": validate_prototype_data_freshness(),
        "frontendFiles": {
            "indexLoadsScheduleData": './all-city-schedule-data.js' in (FRONTEND_DIR / "index.html").read_text(encoding="utf-8"),
            "appReadsScheduleData": "window.ALL_CITY_SCHEDULE_DATA" in (FRONTEND_DIR / "app.js").read_text(encoding="utf-8"),
            "indexLoadsPrototypeData": './prototype-data.js' in (FRONTEND_DIR / "index.html").read_text(encoding="utf-8"),
            "appReadsPrototypeData": "window.PROTOTYPE_RAW_DATA" in (FRONTEND_DIR / "app.js").read_text(encoding="utf-8"),
        },
    }
    checks["status"] = "pass" if (
        checks["scheduleData"]["status"] == "pass"
        and checks["wechatAssets"]["status"] == "pass"
        and checks["prototypeDataFreshness"]["status"] == "pass"
        and checks["frontendFiles"]["indexLoadsScheduleData"]
        and checks["frontendFiles"]["appReadsScheduleData"]
        and checks["frontendFiles"]["indexLoadsPrototypeData"]
        and checks["frontendFiles"]["appReadsPrototypeData"]
    ) else "needs_attention"
    report["endToEndChecks"] = checks
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    return 0 if checks["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
