#!/usr/bin/env python3
"""Data integrity regression tests for the hospital registry pipeline.

Run this before merging data changes to catch:
- Missing source entries
- Unreferenced WeChat QR assets
- Orphan WeChat entry IDs (reference hospital IDs not in registry)
- Cross-file consistency (regional data mirrors Beijing field shape)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from registry_parser import parse_all_city_registries  # noqa: E402

ROOT = SCRIPT_DIR.parent
FRONTEND_DIR = ROOT / "frontend-prototype"
WECHAT_FILE = FRONTEND_DIR / "wechat-entries.js"
REGIONAL_CITY_FILE = FRONTEND_DIR / "regional-city-data.js"
WECHAT_ASSET_DIR = FRONTEND_DIR / "assets" / "wechat-qrcodes"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_registry_source_coverage() -> int:
    registries = parse_all_city_registries()
    errors = 0
    for city, hospitals in registries.items():
        missing = [h["id"] for h in hospitals if not h.get("officialSite")]
        if missing:
            print(f"[FAIL] {city}: {len(missing)} hospitals missing source entry: {missing}")
            errors += 1
        else:
            print(f"[PASS] {city}: {len(hospitals)} hospitals, all have source entries")
    return errors


def test_wechat_asset_references() -> int:
    errors = 0
    texts = [read_text(WECHAT_FILE)]
    if REGIONAL_CITY_FILE.exists():
        texts.append(read_text(REGIONAL_CITY_FILE))

    referenced = set()
    for text in texts:
        for path in re.findall(r'qrImageUrl:\s*"([^"]+)"', text):
            if path.startswith("assets/"):
                referenced.add((FRONTEND_DIR / path).resolve())

    missing = [str(p.relative_to(FRONTEND_DIR)) for p in referenced if not p.exists()]
    if missing:
        print(f"[FAIL] {len(missing)} referenced QR assets missing: {missing}")
        errors += 1
    else:
        print(f"[PASS] {len(referenced)} referenced QR assets all exist")

    # Also check for unreferenced files that might be stale candidates
    if WECHAT_ASSET_DIR.exists():
        existing = {p.resolve() for p in WECHAT_ASSET_DIR.iterdir() if p.is_file()}
        unreferenced = existing - referenced
        if unreferenced:
            print(f"[WARN] {len(unreferenced)} assets in wechat-qrcodes/ not referenced by any entry file: "
                  f"{[p.name for p in sorted(unreferenced)][:10]}")
    return errors


def test_wechat_orphan_ids() -> int:
    registries = parse_all_city_registries()
    errors = 0

    wechat_maps = {"北京": read_text(WECHAT_FILE)}
    if REGIONAL_CITY_FILE.exists():
        regional = read_text(REGIONAL_CITY_FILE)
        for city, variable in (("上海", "SHANGHAI_WECHAT_ENTRIES"), ("深圳", "SHENZHEN_WECHAT_ENTRIES"), ("杭州", "HANGZHOU_WECHAT_ENTRIES")):
            found = re.search(rf"window\.{variable}\s*=\s*\{{(?P<body>.*?)\}};", regional, re.S)
            if found:
                wechat_maps[city] = found.group("body")

    for city, text in wechat_maps.items():
        we_ids = set(re.findall(r"^\s{2}([A-Za-z0-9_]+):\s*\[", text, re.M))
        reg_ids = {h["id"] for h in registries.get(city, [])}
        orphans = we_ids - reg_ids
        if orphans:
            print(f"[FAIL] {city}: WeChat entries reference {len(orphans)} IDs not in registry: {sorted(orphans)}")
            errors += 1
        else:
            print(f"[PASS] {city}: {len(we_ids)} WeChat-referenced hospitals all exist in registry")
    return errors


def test_regional_data_field_consistency() -> int:
    errors = 0
    if not REGIONAL_CITY_FILE.exists():
        print("[SKIP] regional-city-data.js not found")
        return 0

    text = read_text(REGIONAL_CITY_FILE)
    beijing_text = read_text(FRONTEND_DIR / "beijing-3a-hospitals.js")
    beijing_fields = set(re.findall(r'\s{2,4}(\w+):\s*"', beijing_text))

    for city, var in ("上海", "SHANGHAI"), ("深圳", "SHENZHEN"), ("杭州", "HANGZHOU"):
        found = re.search(rf"window\.{var}_3A_HOSPITALS\s*=\s*\[(?P<body>.*?)\];", text, re.S)
        if not found:
            continue
        body = found.group("body")
        regional_fields = set(re.findall(r'\s{2,4}(\w+):\s*"', body))
        missing_fields = beijing_fields - regional_fields
        if missing_fields:
            print(f"[WARN] {city}: fields missing compared to Beijing registry: {missing_fields}")
        else:
            print(f"[PASS] {city}: field shape matches Beijing registry")
    return errors


def test_payload_integrity() -> int:
    errors = 0
    texts = [read_text(WECHAT_FILE)]
    if REGIONAL_CITY_FILE.exists():
        texts.append(read_text(REGIONAL_CITY_FILE))

    for text in texts:
        payloads = re.findall(r'qrPayload:\s*"([^"]+)"', text)
        for p in payloads:
            if p and not (
                p.startswith("http://weixin.qq.com/")
                or p.startswith("https://weixin.qq.com/")
                or p.startswith("https://mp.weixin.qq.com/")
            ):
                print(f"[FAIL] Invalid qrPayload: {p[:120]}")
                errors += 1
    if errors == 0:
        print(f"[PASS] All qrPayload values are valid WeChat URLs")
    return errors


def main() -> int:
    total_errors = 0
    tests = [
        ("Registry source coverage", test_registry_source_coverage),
        ("WeChat asset references", test_wechat_asset_references),
        ("WeChat orphan IDs", test_wechat_orphan_ids),
        ("Regional data field consistency", test_regional_data_field_consistency),
        ("QR payload integrity", test_payload_integrity),
    ]

    for name, func in tests:
        print(f"\n--- {name} ---")
        try:
            errors = func()
            total_errors += errors
        except Exception as exc:
            print(f"[ERROR] {name} raised: {exc}")
            total_errors += 1

    print(f"\n{'='*40}")
    if total_errors == 0:
        print("All tests passed.")
        return 0
    print(f"{total_errors} test failures.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
