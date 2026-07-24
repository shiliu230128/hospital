# 医院挂号入口比选助手

比较北京、上海、深圳、杭州主要医院（三甲/三级）的**官方挂号入口**和**已核验微信小程序/公众号二维码**，帮助快速选择挂号渠道。

在线版：部署到 GitHub Pages 后自动获得 `https://<用户名>.github.io/hospital/` 地址。

---

## 能做什么 / 不能做什么

| 能做的 | 目前还不能做的 |
|---|---|
| 按城市、区县、街道切换医院列表 | 查看某个医生某个日期的实时余号 |
| 查看每家医院的官网挂号地址 | 在线预约挂号 |
| 查看已核验的微信公众号/小程序二维码（可点击放大） | 保证每家医院都有微信入口（没核验到的就留空） |
| 按街道参考点排序找到最近的医院 | 使用浏览器 GPS 自动定位 |
| 对比两家医院的入口 | 查看完整科室排班表（仅北京有少量样本） |
| 查看每天自动更新的数据审计报告 | — |

---

## 怎么使用

### 方式一：在线直接使用（无需安装）

打开项目的 GitHub Pages 地址，选择城市和参考街道，就能查看医院排名和入口。

### 方式二：在自己电脑上运行

**前提：电脑已安装 Python 3.9+**

```bash
# 1. 进入项目目录
cd /path/to/hospital

# 2. 安装 Python 依赖（只需要一次）
pip install -r requirements.txt

# 3. 运行数据刷新（快速模式，几秒完成）
python3 data-access-research/update_data_once.py

# 4. 打开网页
open frontend-prototype/index.html
# Windows：直接双击 frontend-prototype/index.html
```

或一键运行：

```bash
bash scripts/refresh-local.sh
```

运行后会在 `frontend-prototype/generated/` 下产生 2 个自动生成的文件（每次都覆盖，不会越积越多）。

**完整联网刷新（耗时 2-5 分钟）：**

```bash
python3 data-access-research/update_data_once.py --with-wechat-fetch
```

---

## 城市数据现状

| 城市 | 医院数 | 微信入口 | 公开排班 |
|---|---|---|---|
| 北京 | 57 家 | 28 家医院已核验 | 11 家医院共 1847 条 L1 排班 |
| 上海 | 33 家 | 10 家医院已核验 | 3 家医院共 543 条 L1 排班 |
| 深圳 | 23 家 | 3 家医院已核验 | 1 家医院共 69 条 L1 周排班 |
| 杭州 | 18 家 | 6 家医院已核验 | 2 家医院共 400 条 L1 排班 |

公开排班 = 医院官网公开发布的门诊安排，不是实时余号。

**微信二维码规则**：只有从医院官网找到并成功扫码解码为微信入口的才会放上去。官网访问不稳定或首页没放二维码的医院，微信区域留空。

---

## 数据来源

所有数据仅来自：
- 医院官方首页
- 政府/卫健委公开医疗机构信息
- 高校附属医院名单页

**不使用的数据**：非官方汇总网站、百度百科、未核验的第三方链接。

每家医院至少有一条"官方"或"公开机构页"来源；无法确认自有官网的，会写明数据来自政府/高校公开页而非医院官网。

---

## 每天自动刷新

项目已包含 GitHub Actions 工作流（`.github/workflows/refresh-and-deploy.yml`）。

放入你自己的 GitHub 仓库并启用 GitHub Pages 后：
- 每天凌晨自动刷新数据
- 刷新后自动部署网页
- 普通用户打开 GitHub Pages 地址即可看到最新数据

---

## 项目结构（非技术人员只需关注前 3 个）

| 文件/目录 | 用途 |
|---|---|
| `frontend-prototype/index.html` | 网页主文件，双击即可打开 |
| `frontend-prototype/app.js` | 前端交互逻辑 |
| `frontend-prototype/styles.css` | 页面样式 |
| `frontend-prototype/beijing-3a-hospitals.js` | 北京医院基础数据 |
| `frontend-prototype/regional-city-data.js` | 上海/深圳/杭州医院数据和微信入口 |
| `frontend-prototype/wechat-entries.js` | 北京微信入口 |
| `frontend-prototype/location-points.js` | 街道坐标参考点 |
| `frontend-prototype/assets/wechat-qrcodes/` | 已解码的微信二维码图片 |
| `data-access-research/update_data_once.py` | 数据刷新和审计脚本 |
| `data-access-research/test_registry_integrity.py` | 数据完整性回归测试 |
| `data-access-research/update-report.json` | 最新审计结果 |
| `scripts/refresh-local.sh` | 本地一键刷新脚本 |
| `.github/workflows/refresh-and-deploy.yml` | GitHub Actions 自动部署 |
| `docs/` | 产品设计、数据来源、运维说明 |

---

## 常见问题

**Q：为什么有些医院没有公众号二维码？**
A：只有从医院官网首页找到并成功扫码解码为微信入口的才会放上去。

**Q：为什么切换城市后"距离排序"没用？**
A：需要先在页面顶部选择你的街道/乡镇作为参考点，然后选择"距离近"排序。

**Q：能不能在线挂号？**
A：不能。这个工具只帮你在多个入口之间选择，真正的挂号需在官网上完成。

**Q：运行脚本报 `No such file or directory`？**
A：说明你不在项目目录里。先 `cd /path/to/hospital` 再运行命令。

**Q：数据多久更新一次？**
A：GitHub Actions 每天自动刷新。本地使用需手动运行刷新脚本。

---

更多说明：
- 产品边界：`docs/product.md`
- 数据来源和可信度：`docs/data-sources.md`
- 运维和自动化：`docs/operations.md`
