# 医院挂号入口比选助手

这是一个静态网页工具，用来整理和比较重点城市三级甲等/三级医院的官方挂号入口。

默认展示北京。用户可以在页面顶部切换到上海、深圳、杭州；切换城市后，区县、街道/乡镇参考点、医院列表、医院坐标、微信入口和公开排班状态都会按当前城市刷新，不会把所有城市混在一起展示。

它的核心价值不是“帮你直接挂上号”，而是把分散在医院官网、微信服务号/公众号、小程序、114 或本地预约平台等渠道里的入口集中到一个页面里，方便用户快速筛选、比较和跳转到官方渠道确认。

## 先解决一个最常见问题

如果你的终端提示：

```text
No such file or directory
```

通常是因为你当前不在项目目录里。比如终端显示：

```text
your-name@your-computer ~ %
```

这里的 `~` 不是项目目录，所以直接运行 `bash scripts/refresh-local.sh` 会找不到文件。

如果你已经进入项目目录，可以直接运行下面这条命令：

```bash
bash scripts/refresh-local.sh
```

或者先进入项目目录，再运行相对路径命令：

```bash
cd /path/to/hospital
bash scripts/refresh-local.sh
```

## 打开网页

进入项目目录后直接打开：

```bash
open frontend-prototype/index.html
```

也可以在 Finder 里双击：

```text
frontend-prototype/index.html
```

## 页面可以做什么

现在可以做：

- 默认查看北京医院官方/权威挂号入口。
- 切换到上海、深圳、杭州后，刷新为该城市的目标医院、区县、街道和坐标数据。
- 按医院名、科室词、区县筛选。
- 选择街道/乡镇作为位置参考点，按到医院的近似直线距离排序。
- 查看医院官网或权威公开挂号/机构入口。
- 查看已核验的微信服务号、公众号、小程序入口名称或二维码。
- 对比多个候选医院，逐个打开官方入口确认。
- 查看四个城市少量已接入医院的公开出诊样本。
- 查看最近一次数据刷新时间和审计状态。

这些能力适合：

- 用户不知道应该从哪个官方入口挂号。
- 用户想先比较几家医院，再去官方渠道确认。
- 用户只想按城市、区域、距离、科室方向快速缩小候选范围。
- 用户需要给家人找入口，减少反复打开医院官网和公众号的成本。

## 页面不能承诺什么

当前不能承诺：

- 哪个医生现在一定有号。
- 某个日期、上午/下午一定可约。
- 剩余号源数量。
- 自动预约、抢号、刷号。
- 帮用户登录医院、114、微信或 App。

原因是：公开网页通常能稳定拿到的是医院入口和公开出诊安排，不是医生级实时可挂状态。只有拿到授权或稳定合规的 L3/L4 数据源后，才适合做“只看可挂”“最近可约”“剩余号源排序”。

## 城市数据现状

当前城市覆盖：

- 北京：57 家医院入口、已核验微信入口、街道/乡镇参考点、医院坐标；当前自动发现 11 家医院、1847 条 L1 公开排班。
- 上海：33 家目标医院入口、已核验官网二维码解码的微信入口、街道/镇参考点、医院坐标；当前自动发现 3 家医院、543 条 L1 公开排班。
- 深圳：23 家目标医院入口、已核验官网二维码解码的微信入口、街道参考点、医院坐标；当前自动发现 1 家医院、69 条 L1 周排班。
- 杭州：18 家目标医院入口、已核验官网二维码解码的微信入口、街道/镇参考点、医院坐标；当前接入 2 家医院、400 条 L1 公开排班，其中浙江妇保来自官网公开 API。

新城市微信二维码规则和北京一致：没有从医院官网核验到真实二维码或 `qrPayload` 时，不生成假二维码。

这些排班都是官网公开出诊安排或公开接口线索，不等于登录后的实时余号，也不保证下单时一定可约。

## 刷新数据

### 快速刷新，推荐日常使用

```bash
bash scripts/refresh-local.sh
```

这个命令会：

- 检查医院名单和入口数据。
- 探测部分官方来源是否还能访问。
- 抓取并写入全城市公开排班数据。
- 校验前端排班数据、微信二维码资产和页面加载关系。
- 生成最新刷新报告。
- 自动打开网页。

终端会显示 `[update]` 和 `[pipeline]` 开头的进度，不会长时间空白。测试时如果不想自动打开网页，可以运行：

```bash
HOSPITAL_SKIP_OPEN=1 bash scripts/refresh-local.sh
```

### 只刷新审计报告

```bash
python3 data-access-research/update_data_once.py
```

如果想跑完整本地刷新但不自动打开页面，请使用：

```bash
HOSPITAL_SKIP_OPEN=1 bash scripts/refresh-local.sh
```

### 完整联网刷新

```bash
python3 data-access-research/update_data_once.py --with-wechat-fetch
```

完整刷新会重新访问四个城市中已确认的医院官网，抓取微信入口候选和候选二维码，可能需要几分钟。权威公开页和未核验入口会跳过；抓到的候选不会自动展示给用户，仍需要人工核验后才能进入正式入口数据。

## 别人下载后怎么运行

如果别人从 GitHub 或其它平台下载这个项目，需要先进入项目目录。

示例：

```bash
cd /path/to/hospital
bash scripts/refresh-local.sh
```

如果只是想打开页面：

```bash
cd /path/to/hospital
open frontend-prototype/index.html
```

其中 `/path/to/hospital` 要换成他自己电脑上的项目路径。

## 数据从哪里来

项目使用几类数据：

- 医院基础信息：医院官网、政府/卫健委公开机构信息、人工核验整理。
- 目标覆盖审计：脚本会检查北京、上海、深圳、杭州各自的目标医院 seed 是否还有缺口。
- 官方入口：医院官网、公开挂号说明；无法确认自有官网时，只展示权威公开机构页。
- 微信入口：医院官网公开的二维码、微信服务入口或官方说明。
- 公开出诊样本：部分医院官网公开排班页面、周排班表或公开接口；当前北京、上海、深圳、杭州均已有少量 L1 样本。
- 位置数据：街道/乡镇参考点和医院近似坐标。

数据可信规则：

- 不用未核验链接生成假二维码。
- 新抓到的微信候选先进入候选报告，不直接展示。
- 公开出诊安排不等于实时余号。
- 距离排序是近似距离，不是导航路线，也不是自动定位。

## 自动刷新和线上访问

项目已经包含 GitHub Actions 配置：

```text
.github/workflows/refresh-and-deploy.yml
```

如果项目放到你自己的 GitHub 仓库，并启用 GitHub Pages：

- GitHub Actions 会每天北京时间凌晨 2:30 自动运行完整刷新。
- 刷新后会把 `frontend-prototype/` 发布成网页。
- 普通用户打开 GitHub Pages 地址时，会看到最近一次自动发布的数据。

首次启用步骤：

1. 把项目推送到 GitHub 仓库。
2. 打开仓库 `Settings -> Pages`。
3. 发布源选择 `GitHub Actions`。
4. 到 `Actions` 页面手动运行一次 `Refresh and deploy hospital data`。
5. 之后每天凌晨自动刷新。

不需要自己买服务器。GitHub Actions 负责定时运行，GitHub Pages 负责托管网页。

## 项目结构

```text
frontend-prototype/                  前端页面
  index.html                         页面入口
  app.js                             页面交互逻辑
  styles.css                         页面样式
  beijing-3a-hospitals.js            北京医院名单和官方/权威公开入口
  wechat-entries.js                  北京已核验微信入口
  location-points.js                 北京街道/乡镇参考点和医院坐标
  regional-city-data.js              上海、深圳、杭州数据和多城市聚合入口
  generated/                         自动生成的刷新报告

data-access-research/                数据脚本和样本
  update_data_once.py                本地和 GitHub Actions 共用的刷新入口
  fetch_wechat_qr_candidates.py      微信候选入口抓取脚本
  all_city_data_pipeline.py          全城市公开排班发现、解析和前端数据写入
  validate_all_city_pipeline.py      全城市排班和前端资产校验
  parse_*.py                         北京早期公开排班样本解析脚本
  *_sample.json                      少量公开排班样本数据
  update-report.json                 最近一次审计报告

scripts/
  refresh-local.sh                   本地快速刷新并打开页面

docs/
  product.md                         产品目标、使用场景、功能边界
  data-sources.md                    数据来源、可信度、实时号源限制
  operations.md                      本地刷新、自动部署、文件保留规则
```

## 更多说明

- 产品边界：`docs/product.md`
- 数据来源和可信度：`docs/data-sources.md`
- 运行、自动化和文件保留：`docs/operations.md`
