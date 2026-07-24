#!/usr/bin/env python3
"""Find WeChat/QR entry candidates from hospital official homepages.

This script is intentionally conservative: it discovers candidate links and
images from official hospital sites, then writes them for manual verification
before they are promoted into frontend-prototype/wechat-entries.js.
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


KEYWORDS = (
    "微信",
    "公众号",
    "服务号",
    "订阅号",
    "二维码",
    "互联网医院",
    "wechat",
    "weixin",
    "wx",
    "qr",
    "ewm",
)


class CandidateParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.candidates: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key.lower(): value or "" for key, value in attrs}
        joined = " ".join([tag, *attr_map.keys(), *attr_map.values()]).lower()
        if not any(keyword.lower() in joined for keyword in KEYWORDS):
            return

        url = attr_map.get("src") or attr_map.get("data-src") or attr_map.get("href") or ""
        if url:
            url = urllib.parse.urljoin(self.base_url, url)

        self.candidates.append(
            {
                "tag": tag,
                "url": url,
                "alt": attr_map.get("alt", ""),
                "title": attr_map.get("title", ""),
                "class": attr_map.get("class", ""),
                "id": attr_map.get("id", ""),
            }
        )


def parse_hospital_blocks(text: str, city: str) -> list[dict]:
    object_pattern = re.compile(r"\{\s*id:\s*\"(?P<id>[^\"]+)\".*?entries:\s*\[(?P<entries>.*?)\]\s*,?\s*\}", re.S)
    hospitals = []
    for match in object_pattern.finditer(text):
        block = match.group(0)
        name_match = re.search(r'name:\s*"([^"]+)"', block)
        short_match = re.search(r'shortName:\s*"([^"]+)"', block)
        web_match = re.search(r'\{\s*type:\s*"web".*?\}', match.group("entries"), re.S)
        if not web_match:
            continue
        web_block = web_match.group(0)
        url_match = re.search(r'url:\s*"([^"]+)"', web_block)
        status_match = re.search(r'status:\s*"([^"]+)"', web_block)
        if not url_match:
            continue
        hospitals.append(
            {
                "city": city,
                "id": match.group("id"),
                "name": name_match.group(1) if name_match else match.group("id"),
                "shortName": short_match.group(1) if short_match else name_match.group(1) if name_match else match.group("id"),
                "officialSite": url_match.group(1),
                "officialSiteStatus": status_match.group(1) if status_match else "",
            }
        )
    return hospitals


def parse_hospitals(registry_file: Path) -> list[dict]:
    return parse_hospital_blocks(registry_file.read_text(encoding="utf-8"), "北京")


def parse_regional_hospitals(regional_registry_file: Path) -> list[dict]:
    if not regional_registry_file.exists():
        return []

    text = regional_registry_file.read_text(encoding="utf-8")
    city_arrays = {
        "上海": "SHANGHAI_3A_HOSPITALS",
        "深圳": "SHENZHEN_3A_HOSPITALS",
        "杭州": "HANGZHOU_3A_HOSPITALS",
    }
    hospitals = []
    for city, variable_name in city_arrays.items():
        found = re.search(rf"window\.{variable_name}\s*=\s*\[(?P<body>.*?)\];", text, re.S)
        if found:
            hospitals.extend(parse_hospital_blocks(found.group("body"), city))
    return hospitals


def fetch_html(url: str, timeout: int) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 registration-research/0.3",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path)


def download_file(url: str, output_dir: Path, repo_root: Path, hospital_id: str, index: int, timeout: int) -> str:
    parsed = urllib.parse.urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix not in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
        suffix = ".img"
    target = output_dir / f"{hospital_id}-{index}{suffix}"
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 registration-research/0.3"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        target.write_bytes(response.read())
    return repo_relative(target, repo_root)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="../frontend-prototype/beijing-3a-hospitals.js")
    parser.add_argument("--regional-registry", default="../frontend-prototype/regional-city-data.js")
    parser.add_argument("--output", default="wechat_entry_candidates.json")
    parser.add_argument("--asset-dir", default="../frontend-prototype/assets/wechat-qrcodes")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--timeout", type=int, default=12)
    parser.add_argument("--sleep", type=float, default=0.4)
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    repo_root = base_dir.parent
    registry_file = (base_dir / args.registry).resolve()
    regional_registry_file = (base_dir / args.regional_registry).resolve() if args.regional_registry else None
    output_file = (base_dir / args.output).resolve()
    asset_dir = (base_dir / args.asset_dir).resolve()
    if args.download:
        asset_dir.mkdir(parents=True, exist_ok=True)

    hospitals = parse_hospitals(registry_file)
    if regional_registry_file:
        hospitals.extend(parse_regional_hospitals(regional_registry_file))

    results = []
    for hospital in hospitals:
        item = {**hospital, "candidates": [], "error": ""}
        if hospital.get("officialSiteStatus") != "official":
            item["skipped"] = True
            item["skipReason"] = "source entry is not a verified hospital homepage"
            results.append(item)
            continue
        try:
            html = fetch_html(hospital["officialSite"], args.timeout)
            parser_obj = CandidateParser(hospital["officialSite"])
            parser_obj.feed(html)
            for index, candidate in enumerate(parser_obj.candidates):
                if args.download and candidate["url"]:
                    try:
                        candidate["localPath"] = download_file(
                            candidate["url"], asset_dir, repo_root, hospital["id"], index, args.timeout
                        )
                    except Exception as exc:  # noqa: BLE001
                        candidate["downloadError"] = str(exc)
                item["candidates"].append(candidate)
        except Exception as exc:  # noqa: BLE001
            item["error"] = str(exc)
        results.append(item)
        time.sleep(args.sleep)

    output_file.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {output_file}")


if __name__ == "__main__":
    main()
