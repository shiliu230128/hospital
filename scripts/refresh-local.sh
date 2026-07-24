#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[local] 开始刷新数据审计。"
echo "[local] 默认不重抓微信候选，通常几十秒内完成。"
python3 data-access-research/update_data_once.py --skip-wechat-fetch

echo "[local] 刷新全城市公开排班数据。"
python3 data-access-research/all_city_data_pipeline.py \
  --timeout 10 \
  --sleep 0.2 \
  --max-pages-per-hospital 5 \
  --max-records-per-hospital 200

echo "[local] 校验前端数据包。"
python3 data-access-research/validate_all_city_pipeline.py

if [[ "${HOSPITAL_SKIP_OPEN:-0}" == "1" ]]; then
  echo "[local] 已跳过自动打开页面。"
else
  echo "[local] 打开前端页面。"
  open frontend-prototype/index.html
fi
