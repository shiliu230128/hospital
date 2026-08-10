# 数据来源说明

## 数据原则

本项目只把可核验、低风险的数据展示给用户。

- 医院官网、114、本地预约平台、医院公开页面、医院官方微信公众号/服务号/小程序说明优先。
- 微信二维码必须来自医院官网公开页面，或由官网二维码解码得到真实 `qrPayload`。
- 不使用未核验链接生成假公众号二维码。
- 新抓到的候选入口只进入候选报告，不自动进入正式前端。
- 新城市先接入 L0 入口和位置比选；没有稳定公开排班源时不复用其它城市样本。
- 多城市 registry 审计同时检查“已有医院是否有来源”和“目标 seed 是否仍有缺口”。

## 当前城市覆盖

- 北京：目标医院、官方/权威公开入口、已核验微信入口、街道/乡镇参考点、医院坐标、部分官网公开排班。
- 上海：目标 seed 医院、官方/权威公开入口、官网二维码解码得到的微信入口、街道/镇参考点、医院坐标、部分官网公开排班。
- 深圳：目标 seed 医院、官方/权威公开入口、官网二维码解码得到的微信入口、街道参考点、医院坐标、深圳市人民医院官网周排班。
- 杭州：目标 seed 医院、官方/权威公开入口、官网二维码解码得到的微信入口、街道/镇参考点、医院坐标、邵逸夫医院官网排班和浙江妇保公开排班 API。

当前公开排班覆盖仍是少量医院，不代表城市内所有医院都能取得 L1 数据；未覆盖医院仍可使用官方入口、城市筛选、街道距离排序和医院对比。

## 当前数据类型

### 医院 registry

文件：

- `frontend-prototype/beijing-3a-hospitals.js`
- `frontend-prototype/regional-city-data.js`

包含：

- 医院名称和简称。
- 城市和区县。
- 地址。
- 等级和类型。
- registry 置信度。
- 官方/权威公开入口。

三级但三甲评级未核验的医院会保留 `medium` 置信度，并在等级中明确标注。

### 微信入口

文件：

- `frontend-prototype/wechat-entries.js`
- `frontend-prototype/regional-city-data.js`

包含已核验或可从官网识别的：

- 微信公众号。
- 服务号。
- 小程序。
- 二维码图片或真实二维码 payload。
- 来源 URL。
- 可挂号能力判断。

候选抓取结果在 `data-access-research/wechat_entry_candidates.json`，不等于正式数据。

新城市如果只识别到官方微信入口名称，但没有核验到二维码图片或真实 `qrPayload`，会只展示入口名称或留作待抓取，不生成二维码。

### 位置参考

文件：

- `frontend-prototype/location-points.js`
- `frontend-prototype/regional-city-data.js`

包含：

- 当前医院所在区的街道/乡镇级参考点。
- 医院院区近似坐标。

距离排序使用用户手动选择的位置参考点计算，不做浏览器自动定位。

### 公开排班样本

文件：

- `data-access-research/bch_schedule_sample.json`
- `data-access-research/puh3_pediatrics_schedule_sample.json`
- `data-access-research/pumch_dockervisit_sample_excerpt.json`
- `frontend-prototype/prototype-data.js`

当前已验证过以下公开出诊样本类型：

- 北京儿童医院官网公开出诊表。
- 北京大学第三医院官网公开接口。
- 北京协和医院官网公开出诊片段。
- 北京、上海、杭州部分医院官网 HTML 周排班表。
- 深圳市人民医院官网周期出诊表。
- 浙江大学医学院附属妇产科医院官网公开排班 API。

这些数据属于 L1 公开出诊安排，不等于实时余号。

## 不能承诺实时余号的原因

多数医院真实挂号能力通常在登录、小程序、App、授权接口或防护后的页面中。当前公开网页能稳定获取的主要是入口和部分排班，不是医生级实时可挂状态。

因此：

- `未停诊` 不等于 `可预约`。
- `门诊限号` 不等于 `剩余号源`。
- 页面上不能显示“只看有号”或“剩余号源排序”，除非数据源达到 L3/L4。

## 自动刷新会更新什么

`data-access-research/update_data_once.py` 会刷新：

- 来源健康探测。
- 北京名单审计和多城市 registry 覆盖审计，包括目标 seed 缺口检测。
- 四个城市已确认医院官网的微信候选抓取，完整模式下。
- 未引用候选二维码清理。
- 微信正式入口校验。
- 公开排班样本摘要。
- 前端可读取的最新刷新报告。
- `frontend-prototype/prototype-data.js` 里的嵌入式公开排班样本包。

它不会自动把未核验的新医院、新二维码、新公众号写进正式前端数据。

全城市公开排班由 `data-access-research/all_city_data_pipeline.py` 单独生成，并由 `data-access-research/validate_all_city_pipeline.py` 校验后写入 `frontend-prototype/all-city-schedule-data.js`。
