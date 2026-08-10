#!/usr/bin/env python3
"""Shared hospital registry parser used by update_data_once.py, all_city_data_pipeline.py,
and test_registry_integrity.py to avoid code duplication and import-cycle risk."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT / "frontend-prototype"
REGISTRY_FILE = FRONTEND_DIR / "beijing-3a-hospitals.js"
REGIONAL_CITY_FILE = FRONTEND_DIR / "regional-city-data.js"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


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
