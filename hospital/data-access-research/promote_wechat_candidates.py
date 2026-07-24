#!/usr/bin/env python3
"""Download high-signal WeChat QR candidates from hospital own domains and decode them.

This step never rewrites frontend registry files by itself. It writes:
  data-access-research/wechat-candidate-decoded.json

Only candidates whose image URL is served by the hospital's own domain and whose
filename hints QR intent (ewm/qr/wx/erweima) are considered. Everything else is
left for manual verification.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, "/tmp/hospital_qrdeps")

import cv2  # type: ignore
import numpy as np  # type: ignore


QR_HINTS = re.compile(r"(ewm|erweima|qrcode|qr|wx|weixin|wechat)", re.I)
BAD_HINTS = re.compile(r"(share|logo|banner|nav_icon|jweixin\.min|weixinshare)", re.I)


def is_probable_qr(candidate: dict, own_host: str) -> bool:
    url = candidate.get("url", "")
    if not url or not url.lower().startswith(("http://", "https://")):
        return False
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc.lower() != own_host.lower():
        return False
    tail = (parsed.path.rsplit("/", 1)[-1] or "").lower()
    if not tail.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
        return False
    if BAD_HINTS.search(url):
        return False
    haystack = " ".join([
        candidate.get("alt", ""),
        candidate.get("title", ""),
        candidate.get("class", ""),
        candidate.get("id", ""),
        url,
    ]).lower()
    return bool(QR_HINTS.search(haystack))


def download(url: str, target: Path, timeout: int) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 registration-research/0.4"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        target.write_bytes(response.read())


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path)


def decode(path: Path) -> str:
    data = np.frombuffer(path.read_bytes(), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        return ""
    detector = cv2.QRCodeDetector()
    payload, _, _ = detector.detectAndDecode(img)
    if payload:
        return payload
    for scale in (1.5, 2.0, 3.0):
        resized = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        payload, _, _ = detector.detectAndDecode(resized)
        if payload:
            return payload
    return ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+", required=True)
    parser.add_argument("--asset-dir", default="../frontend-prototype/assets/wechat-qrcodes")
    parser.add_argument("--output", default="wechat-candidate-decoded.json")
    parser.add_argument("--timeout", type=int, default=8)
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    repo_root = base_dir.parent
    asset_dir = (base_dir / args.asset_dir).resolve()
    asset_dir.mkdir(parents=True, exist_ok=True)
    output_file = (base_dir / args.output).resolve()

    results = []
    for input_path in args.inputs:
        entries = json.loads(Path(input_path).read_text(encoding="utf-8"))
        for hospital in entries:
            if hospital.get("skipped") or hospital.get("error"):
                continue
            own_host = urllib.parse.urlparse(hospital.get("officialSite", "")).netloc
            if not own_host:
                continue
            for index, candidate in enumerate(hospital.get("candidates") or []):
                if not is_probable_qr(candidate, own_host):
                    continue
                url = candidate["url"]
                suffix = Path(urllib.parse.urlparse(url).path).suffix.lower() or ".png"
                target = asset_dir / f"{hospital['id']}-{index}{suffix}"
                item = {
                    "city": hospital.get("city"),
                    "hospitalId": hospital["id"],
                    "hospitalName": hospital.get("name"),
                    "candidateUrl": url,
                    "hints": {
                        "alt": candidate.get("alt", ""),
                        "title": candidate.get("title", ""),
                        "class": candidate.get("class", ""),
                        "id": candidate.get("id", ""),
                    },
                    "localPath": repo_relative(target, repo_root),
                    "downloadError": "",
                    "decodedPayload": "",
                    "decodeError": "",
                }
                try:
                    download(url, target, args.timeout)
                except Exception as exc:  # noqa: BLE001
                    item["downloadError"] = str(exc)
                    results.append(item)
                    continue
                try:
                    item["decodedPayload"] = decode(target)
                except Exception as exc:  # noqa: BLE001
                    item["decodeError"] = str(exc)
                results.append(item)

    output_file.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {output_file}; {sum(1 for x in results if x['decodedPayload'])}/{len(results)} decoded")


if __name__ == "__main__":
    main()
