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

## GitHub Pages 自动发布（可选）

仓库已内置：

```text
.github/workflows/refresh-and-deploy.yml
```

它每天北京时间 02:30 自动运行一次，也支持在 GitHub 页面手动运行。

如果你的仓库默认分支不是 `main` 或 `master`，先把 workflow 里的 `push.branches` 改成你的实际分支名，再推送。

这套链路不需要自建服务器：

- GitHub Actions 负责在云端运行 Python，刷新数据文件。
- GitHub Pages 负责托管 `frontend-prototype/` 里的静态网页。
- 用户访问网页时不会现场爬医院官网，而是读取最近一次 Actions 成功生成的数据快照。
- 如果全城市公开排班这次抓取 0 条，workflow 会保留上一版有效 `frontend-prototype/all-city-schedule-data.js`，避免页面被空数据覆盖。

注意：Actions 部署会刷新在线 Pages 站点，但默认不会把每天生成的数据反向提交回 GitHub 仓库源码。仓库文件只会随着你手动提交而变化；在线页面会随着 Actions 部署更新。

首次启用步骤：

1. 把项目 push 到 GitHub 仓库。
2. 进入 `Settings -> Pages`。
3. 将发布源设置为 `GitHub Actions`。
4. 进入 `Actions` 页面。
5. 选择 `Refresh data and deploy Pages`。
6. 点击 `Run workflow`。
7. 第一次成功后，回到 `Settings -> Pages` 查看在线地址。
8. 后续默认每天北京时间 02:30 自动刷新一次。

手动运行时有一个 `with_wechat_fetch` 选项：

- 不勾选：快速刷新，适合日常发布。
- 勾选：会额外抓取微信候选入口，耗时更久，适合你准备人工核验二维码时使用。

如果 Actions 没有自动出现，先确认：

- `.github/workflows/refresh-and-deploy.yml` 已经上传到 GitHub。
- 文件在 `main` 或 `master` 分支上。
- 仓库 `Settings -> Actions -> General` 没有禁用 Actions。
- 仓库 `Settings -> Pages -> Source` 已选择 `GitHub Actions`。

如果 Pages 成功后地址是 404，通常等 1-3 分钟再刷新；第一次部署需要 GitHub 建站。

## GitHub 页面和本地预览的区别

在 GitHub 仓库文件列表里点开 `frontend-prototype/index.html`，看到的是源码，不是网页应用预览。要真正看到页面，有两种方式：

1. 本地下载项目后，双击或打开 `frontend-prototype/index.html`。
2. 启用 GitHub Pages 后，访问 Pages 地址，例如 `https://<你的用户名>.github.io/<仓库名>/`。

本项目的前端数据以 `.js` 文件形式加载，所以本地 `file://` 直接打开可以看到页面。只有运行 Python 刷新脚本时，才需要安装 Python 依赖和联网。

## 输出文件

稳定输出文件：

- `data-access-research/update-report.json`：最近一次完整审计报告。
- `frontend-prototype/prototype-data.js`：本地静态页面直接读取的北京公开排班样本包。
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
cd /path/to/hospital
bash scripts/refresh-local.sh
```

或先进入项目：

```bash
cd /path/to/hospital
```

### 终端看起来没有反应

当前默认快速模式会立即输出 `[update]` 进度。如果运行完整刷新，看到“开始抓取微信候选入口”后等待数分钟是正常的。

### 刷新后验收失败

如果 `validate_all_city_pipeline.py` 报 `emptyCrawl: true`，说明这次全城市公开排班没有抓到任何 L1 记录。脚本会故意返回非 0，提醒检查源站、网络或解析规则。
这种情况下，`all_city_data_pipeline.py` 会保留上一版有效的 `frontend-prototype/all-city-schedule-data.js`，不会把页面刷空。

### 页面为什么没有实时余号

当前没有稳定、授权、医生级实时号源数据。公开排班只能说明曾公开出诊安排，最终能否预约必须进入官方入口确认。

### 为什么有些微信入口没有二维码

只有核验到真实官网二维码或真实二维码 payload 时才展示二维码。只核验到官方微信服务页但没有二维码时，会展示入口名称或链接，不生成假二维码。

### GitHub Actions 能不能自动运行

能。当前仓库已经内置 workflow，只需要仓库启用 Actions，并在 Pages 设置里选择 `GitHub Actions` 作为发布源。这个项目不需要自建服务器。

如果 GitHub 云端访问某些医院官网失败，刷新可能抓不到新公开排班；脚本会保留上一版有效数据，并在 Actions 日志里显示 warning 或失败原因。
