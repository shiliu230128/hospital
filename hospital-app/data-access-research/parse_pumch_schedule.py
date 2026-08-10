#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup


DATE_RE = re.compile(r"(\d{4})[.-](\d{2})[.-](\d{2})\s*(星期[一二三四五六日天])?")
SLOT_NAMES = {"上午", "下午", "晚上", "夜间"}


def text_of(node):
    return " ".join(node.get_text(" ", strip=True).split()) if node else ""


def parse_date_columns(table):
    cells = [text_of(cell) for cell in table.find_all(["td", "th"])]
    date_columns = []
    for cell in cells:
        match = DATE_RE.search(cell)
        if not match:
            continue
        year, month, day, weekday = match.groups()
        weekday = (weekday or "").replace("星期天", "星期日")
        date_columns.append({
            "date": f"{year}-{month}-{day}",
            "weekday": weekday,
            "label": f"{year}-{month}-{day} {weekday}".strip(),
        })
    return date_columns


def parse_schedule(html):
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")

    date_columns = []
    for table in tables:
        date_columns = parse_date_columns(table)
        if date_columns:
            break

    if not date_columns:
        raise RuntimeError("Unable to find PUMCH date columns")

    row_width = len(date_columns)
    sample_rows = []

    for table in tables:
        if parse_date_columns(table):
            continue

        current_department = ""
        for row in table.find_all("tr"):
            cells = [text_of(cell) for cell in row.find_all(["td", "th"])]
            cells = [cell for cell in cells if cell]
            if not cells:
                continue

            if len(cells) >= row_width + 2 and cells[0] not in SLOT_NAMES:
                current_department = cells[0]
                sample_rows.append([current_department, cells[1], *cells[2:2 + row_width]])
                continue

            if len(cells) >= row_width + 1 and current_department:
                sample_rows.append([cells[0], *cells[1:1 + row_width]])

    return {
        "sourceUrl": "https://www.pumch.cn/dsearchs/dockervisit/3/1.html",
        "sourceNote": "北京协和医院官网公开门诊出诊表。该数据为公开排班，不代表实时余号。",
        "tableCount": len(tables),
        "dateColumns": date_columns,
        "sampleRows": sample_rows,
    }


def main():
    if len(sys.argv) != 3:
        print("Usage: parse_pumch_schedule.py <input_html> <output_json>", file=sys.stderr)
        return 2

    html_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    parsed = parse_schedule(html_path.read_text(encoding="utf-8", errors="ignore"))
    output_path.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(parsed['sampleRows'])} rows to {output_path}")


if __name__ == "__main__":
    raise SystemExit(main())
