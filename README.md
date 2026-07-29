医院挂号入口比选助手
一个静态网页工具，集中整理并对比重点城市三级甲等 / 三级医院的官方挂号入口，支持按区域、距离、科室快速筛选，一键跳转官方挂号渠道确认号源。
⚠️ 前置必读：目录层级与路径纠正
原仓库存在双层嵌套结构，直接按默认路径运行会出现 No such file or directory 报错。
从 GitHub 下载 ZIP 解压或克隆仓库后，实际可运行的项目文件位于第二层目录中，完整目录结构如下：
plaintext
hospital-main/              ← 第一层：ZIP 解压后的仓库根目录
├── data-access-research/   # 零散旧文件，可忽略
└── hospital/               ← 第二层：真正的项目根目录（所有操作必须在此目录执行）
    ├── frontend-prototype/ # 前端页面文件
    ├── data-access-research/ # 数据处理脚本
    ├── scripts/            # 快捷执行脚本
    └── docs/               # 详细说明文档
获取正确的项目绝对路径（Mac）
在 Finder 中找到第二层的 hospital 文件夹
按住 Option 键，同时右键点击该文件夹
选择「将 “hospital” 拷贝为路径名称」，即可复制完整绝对路径
打开终端，输入 cd 后粘贴路径，回车即可进入项目目录
Windows 用户可直接在文件夹地址栏复制路径，在终端执行 cd 粘贴的路径 进入。
方式一：直接打开静态页面（零环境依赖）
如果仅需查看已收录的医院挂号入口，不需要更新数据，无需安装任何环境，直接打开前端页面即可使用。
进入第二层 hospital 目录
找到 frontend-prototype/index.html
双击用浏览器打开即可正常使用
终端快捷打开命令（需先进入第二层 hospital 目录）：
bash
# Mac 系统
open frontend-prototype/index.html

# Windows 系统（Git Bash / PowerShell）
start frontend-prototype/index.html
方式二：运行数据刷新脚本
刷新脚本用于校验数据完整性、更新公开排班信息，需提前安装 Python 3 环境。
前置依赖
Python 3.x（终端执行 python3 --version 确认已安装）
Bash 环境（Mac / Linux 原生支持，Windows 推荐使用 Git Bash 或 WSL）
1. 进入正确的项目目录
bash
# 替换为你自己的第二层 hospital 文件夹绝对路径
cd /Users/your-name/Downloads/hospital-main/hospital
2. 快速本地刷新（日常推荐）
仅基于本地已有数据做格式校验、生成刷新报告，不重新爬取医院官网，执行速度快。
脚本运行完成后会自动打开最新页面。
bash
bash scripts/refresh-local.sh
若不需要自动打开浏览器，执行：
bash
HOSPITAL_SKIP_OPEN=1 bash scripts/refresh-local.sh
3. 完整联网刷新（拉取最新数据）
重新访问所有已收录医院的官方网站，抓取最新公开排班、微信入口候选数据，耗时较长（通常数分钟）。
注意：抓取到的微信入口候选需人工核验后才会在前端页面展示，不会直接上线。
bash
python3 data-access-research/update_data_once.py --with-wechat-fetch
仅生成数据审计报告、不执行完整刷新：
bash
python3 data-access-research/update_data_once.py
页面核心功能
支持北京、上海、深圳、杭州四座城市一键切换
按医院名称、科室关键词、所在区县筛选
选择街道 / 乡镇作为参考点，按近似直线距离排序
查看医院官网、官方微信服务号 / 公众号 / 小程序入口
查看已收录医院的公开出诊安排样本
显示最近一次数据刷新时间与审计状态
功能边界说明
本工具仅做官方入口聚合与公开信息参考，不承诺以下能力：
不保证指定医生 / 日期的实时号源、剩余号量
不提供自动预约、抢号、刷号功能
不代用户登录任何医院或挂号平台
距离排序为直线近似距离，非实际导航路线距离
常见问题
Q: 运行脚本提示 No such file or directory
A: 几乎都是因为当前终端停留在第一层 hospital-main 目录，未进入第二层的 hospital 子目录。请参考上文「前置必读」进入正确目录后再执行命令。
Q: 提示 python3: command not found
A: 电脑未安装 Python 3，请先安装 Python 3 并配置好环境变量。
Q: Windows 系统无法运行 bash 脚本
A: 请安装 Git Bash 或启用 WSL 子系统后再执行脚本；仅查看页面的话，直接双击 index.html 文件即可。
Q: 页面打开空白或无数据
A: 确认打开的是 hospital-main/hospital/frontend-prototype/index.html，而非其他目录下的同名文件。
自动部署（GitHub Pages）
项目已内置 GitHub Actions 配置，可实现每日自动刷新数据并发布网页，无需额外购买服务器：
将第二层 hospital 目录的完整内容推送到你的 GitHub 仓库
进入仓库 Settings → Pages，发布源选择 GitHub Actions
进入 Actions 页面，手动运行一次 Refresh and deploy hospital data
后续每日北京时间凌晨 2:30 会自动执行数据刷新并部署页面
数据来源与可信规则
医院基础信息：卫健委公开机构信息、医院官网，人工核验整理
官方挂号入口：医院官网公开渠道、官方微信入口说明
公开排班数据：医院官网公开出诊页面、公开数据接口
可信原则：未核验的入口不生成二维码；公开排班不等于实时可约号源
项目结构
plaintext
hospital/                    # 项目根目录（第二层）
├── frontend-prototype/      # 前端静态页面
│   ├── index.html           # 页面入口
│   ├── app.js               # 页面交互逻辑
│   ├── styles.css           # 样式文件
│   ├── beijing-3a-hospitals.js  # 北京医院基础数据
│   ├── wechat-entries.js    # 北京已核验微信入口
│   ├── location-points.js   # 坐标与街道参考点数据
│   ├── regional-city-data.js # 上海/深圳/杭州多城市数据
│   └── generated/           # 自动生成的刷新报告
├── data-access-research/    # 数据处理脚本
│   ├── update_data_once.py  # 数据刷新入口脚本
│   ├── fetch_wechat_qr_candidates.py # 微信入口抓取脚本
│   ├── all_city_data_pipeline.py    # 排班数据处理流水线
│   ├── validate_all_city_pipeline.py # 数据校验脚本
│   └── *_sample.json        # 公开排班样本数据
├── scripts/
│   └── refresh-local.sh     # 本地快速刷新脚本
└── docs/                    # 详细说明文档
    ├── product.md
    ├── data-sources.md
    └── operations.md
免责声明：本工具仅整理公开官方挂号入口，所有挂号操作与就诊安排请以医院官方渠道最终信息为准。
