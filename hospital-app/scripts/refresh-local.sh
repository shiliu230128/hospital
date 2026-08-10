#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[local] 开始刷新数据审计。"
echo "[local] 默认不重抓微信候选，通常几十秒内完成。"
python3 data-access-research/update_data_once.py --skip-wechat-fetch

echo "[local] 校验前端样本包和刷新产物。"
python3 data-access-research/test_registry_integrity.py

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
  # macOS: 自动用浏览器打开页面
  # Linux: 替换为 xdg-open；Windows: 替换为 start
  if command -v open >/dev/null 2>&1; then
    open frontend-prototype/index.html
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open frontend-prototype/index.html
  else
    echo "[local] 请手动打开 frontend-prototype/index.html"
  fi
fi
