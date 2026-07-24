# 运行和部署说明

## 路径规则

终端命令里的相对路径只在“当前已经进入项目目录”时才有效。

如果终端提示符是：

```text
your-name@your-computer ~ %
```

说明你还在用户主目录，不在项目目录。此时应该使用绝对路径，或先进入项目目录。

本机项目目录是：

```text
/path/to/hospital
```

## 本机直接打开

```bash
open frontend-prototype/index.html
```

页面默认展示北京。切换到上海、深圳、杭州不需要额外命令，前端会从 `frontend-prototype/regional-city-data.js` 读取对应城市数据。

## 本机快速刷新

推荐：

```bash
bash scripts/refresh-local.sh
```

它会刷新审计报告、全城市公开排班数据，校验前端数据包，并自动打开页面。

如果只是测试脚本，不想自动打开浏览器，可以运行：

```bash
HOSPITAL_SKIP_OPEN=1 bash scripts/refresh-local.sh
```

## 本机只刷新审计报告

```bash
python3 data-access-research/update_data_once.py
```

## 本机只刷新全城市排班

```bash
python3 data-access-research/all_city_data_pipeline.py --timeout 10 --sleep 0.2 --max-pages-per-hospital 5 --max-records-per-hospital 200
python3 data-access-research/validate_all_city_pipeline.py
```

## 本机完整联网刷新

```bash
python3 data-access-research/update_data_once.py --with-wechat-fetch
```

完整刷新会访问四个城市中已确认的医院官网并下载微信候选二维码，可能耗时数分钟。权威公开页和未核验入口会跳过，抓取结果会进入 `data-access-research/wechat_entry_candidates.json`，不会自动变成正式入口。

## 别人下载后的通用命令

如果项目在其它路径，需要先进入项目目录：

```bash
cd /path/to/hospital
bash scripts/refresh-local.sh
```

只打开页面：

```bash
cd /path/to/hospital
open frontend-prototype/index.html
```

只刷新不打开：

```bash
cd /path/to/hospital
python3 data-access-research/update_data_once.py
```

## GitHub Pages 自动发布

项目包含 GitHub Actions workflow：

```text
.github/workflows/refresh-and-deploy.yml
```

它会每天北京时间 2:30 运行审计刷新、全城市公开排班刷新和前端数据校验，并把 `frontend-prototype/` 发布到 GitHub Pages。

首次启用步骤：

1. 把项目 push 到 GitHub 仓库。
2. 进入 `Settings -> Pages`。
3. 将发布源设置为 `GitHub Actions`。
4. 进入 `Actions` 页面，手动运行一次 `Refresh and deploy hospital data`。
5. 第一次成功后，后续每天凌晨自动刷新。

## 输出文件

稳定输出文件：

- `data-access-research/update-report.json`：最近一次完整审计报告。
- `frontend-prototype/generated/latest-report.json`：给静态页面或外部工具读取的 JSON。
- `frontend-prototype/generated/latest-report.js`：给本地 `file://` 打开页面直接加载的 JS。
- `data-access-research/all-city-crawl-report.json`：最近一次全城市公开排班抓取报告。
- `frontend-prototype/all-city-schedule-data.js`：前端直接加载的全城市公开排班数据。

这些文件每次运行会覆盖旧内容，不会按时间戳无限新增。

## 冗余产物控制

当前脚本不会主动生成多份历史报告。如果未来新增 `data-access-research/reports/history/*.json` 这类历史文件，`update_data_once.py` 已内置保留机制：默认只保留最新 3 个，删除更旧的文件。

微信候选二维码下载后也会清理：只有 `frontend-prototype/wechat-entries.js` 正式引用的本地二维码会保留，未引用候选会删除。

## 常见问题

### No such file or directory

先看终端当前位置。如果你在 `~` 目录，不能直接运行 `bash scripts/refresh-local.sh`。请改用：

```bash
bash scripts/refresh-local.sh
```

或先进入项目：

```bash
cd /path/to/hospital
```

### 终端看起来没有反应

当前默认快速模式会立即输出 `[update]` 进度。如果运行完整刷新，看到“开始抓取微信候选入口”后等待数分钟是正常的。

### 页面为什么没有实时余号

当前没有稳定、授权、医生级实时号源数据。公开排班只能说明曾公开出诊安排，最终能否预约必须进入官方入口确认。

### 为什么有些微信入口没有二维码

只有核验到真实官网二维码或真实二维码 payload 时才展示二维码。只核验到官方微信服务页但没有二维码时，会展示入口名称或链接，不生成假二维码。

### GitHub Actions 能不能自动运行

能，但前提是项目已经在 GitHub 仓库里，并且仓库启用了 Actions 和 Pages。这个项目不需要自建服务器。
