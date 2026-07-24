const DATA_FILES = {
  bch: "../data-access-research/bch_schedule_sample.json",
  puh3: "../data-access-research/puh3_pediatrics_schedule_sample.json",
  pumch: "../data-access-research/pumch_dockervisit_sample_excerpt.json",
};

// L1 schedule samples (北京 only). These contribute dataLevel:"L1" and schedule-specific
// entry URLs; all other fields (name/level/type/address) come from the authoritative
// registry in beijing-3a-hospitals.js via buildHospitalRegistry().
const L1_SCHEDULE_SAMPLES = [
  {
    id: "bch",
    name: "首都医科大学附属北京儿童医院",
    shortName: "北京儿童医院",
    campusName: "本部",
    district: "西城",
    address: "北京市西城区南礼士路56号",
    level: "三级甲等",
    type: "儿童专科",
    distanceKm: 8.7,
    dataLevel: "L1",
    entries: [
      {
        type: "web",
        name: "医院官网出诊表",
        url: "http://www.bch.com.cn/Html/Hospitals/Schedulings/OPIndex0_0.html",
        status: "official",
      },
      {
        type: "web",
        name: "医院官网",
        url: "http://www.bch.com.cn/",
        status: "official",
      },
      {
        type: "mini",
        name: "医院小程序入口待核验",
        value: "北京儿童医院相关官方小程序",
        status: "manual_unverified",
      },
    ],
  },
  {
    id: "puh3",
    name: "北京大学第三医院",
    shortName: "北医三院",
    campusName: "北京大学第三医院本部",
    district: "海淀",
    address: "北京市海淀区花园北路49号",
    level: "三级甲等",
    type: "综合医院",
    distanceKm: 6.4,
    dataLevel: "L1",
    entries: [
      {
        type: "web",
        name: "官网出停诊信息",
        url: "https://www.puh3.net.cn/yyfw/ctzxx.htm",
        status: "official",
      },
      {
        type: "web",
        name: "公开排班接口来源页",
        url: "https://www.puh3.net.cn/",
        status: "official",
      },
      {
        type: "mini",
        name: "北医三院小程序入口待核验",
        value: "北京大学第三医院",
        status: "manual_unverified",
      },
    ],
  },
  {
    id: "pumch",
    name: "北京协和医院",
    shortName: "协和医院",
    campusName: "东单院区",
    district: "东城",
    address: "北京市东城区帅府园1号",
    level: "三级甲等",
    type: "综合医院",
    distanceKm: 11.6,
    dataLevel: "L1",
    entries: [
      {
        type: "web",
        name: "官网门诊出诊表",
        url: "https://www.pumch.cn/visitinfo.html",
        status: "official",
      },
      {
        type: "web",
        name: "官网挂号说明",
        url: "https://www.pumch.cn/news_visitinfo.html",
        status: "official",
      },
      {
        type: "mini",
        name: "北京协和医院小程序",
        value: "北京协和医院",
        status: "manual_unverified",
      },
    ],
  },
];

const COMMON_ENTRIES = [
  {
    type: "web",
    name: "北京市预约挂号统一平台 114",
    url: "https://www.114yygh.com/",
    status: "official_entry",
  },
  {
    type: "phone",
    name: "114 电话挂号",
    value: "010-114",
    status: "official_entry",
  },
  {
    type: "mini",
    name: "北京114预约挂号小程序/公众号",
    value: "北京114预约挂号",
    status: "official_entry",
  },
];

const DEPARTMENTS = [
  {
    id: "all",
    label: "全部",
    symbol: "全",
    aliases: ["医院", "挂号", "门诊"],
    keywords: [],
  },
  {
    id: "pediatrics",
    label: "儿科",
    symbol: "儿",
    aliases: ["儿童发热", "孩子发烧", "小儿咳嗽", "新生儿", "儿研所"],
    keywords: ["儿", "小儿", "儿童", "新生儿", "儿科", "儿研所"],
  },
  {
    id: "internal",
    label: "内科",
    symbol: "内",
    aliases: ["咳嗽", "胃疼", "糖尿病", "高血压", "肾病"],
    keywords: ["内科", "呼吸", "消化", "心内", "肾内", "内分泌", "血液", "风湿", "神经内", "感染", "过敏反应", "过敏", "免疫", "老年", "干部", "保健", "白血病", "发热"],
  },
  {
    id: "surgery",
    label: "外科",
    symbol: "外",
    aliases: ["甲状腺", "胆囊", "泌尿", "乳腺", "头部外伤"],
    keywords: ["外科", "普外", "泌尿", "胸外", "神经外", "肝胆", "骨外", "乳腺", "血管外", "整形", "烧伤", "肛肠"],
  },
  {
    id: "obgyn",
    label: "妇产",
    symbol: "妇",
    aliases: ["月经", "怀孕", "产检", "不孕"],
    keywords: ["妇", "产", "生殖", "计划生育", "遗传"],
  },
  {
    id: "oncology",
    label: "肿瘤科",
    symbol: "瘤",
    aliases: ["肿瘤", "癌症", "化疗"],
    keywords: ["肿瘤科", "肿瘤中心", "肿瘤门诊"],
  },
  {
    id: "tcm",
    label: "中医科",
    symbol: "中",
    aliases: ["中医", "中药", "针灸", "推拿", "拔罐"],
    keywords: ["中医", "针灸", "推拿", "中西医"],
  },
  {
    id: "rehab",
    label: "康复科",
    symbol: "康",
    aliases: ["康复", "理疗", "术后恢复"],
    keywords: ["康复", "理疗"],
  },
  {
    id: "er",
    label: "急诊/重症",
    symbol: "急",
    aliases: ["急诊", "重症", "ICU", "抢救"],
    keywords: ["急诊", "重症", "ICU", "抢救", "危重"],
  },
  {
    id: "derm",
    label: "皮肤",
    symbol: "皮",
    aliases: ["皮疹", "湿疹", "痤疮", "过敏"],
    keywords: ["皮肤", "性病", "美容"],
  },
  {
    id: "ortho",
    label: "骨科",
    symbol: "骨",
    aliases: ["膝盖疼", "腰椎", "骨折", "运动损伤"],
    keywords: ["骨", "运动医学", "脊柱", "关节"],
  },
  {
    id: "eye",
    label: "眼科",
    symbol: "眼",
    aliases: ["近视", "眼疼", "眼底", "青光眼"],
    keywords: ["眼", "屈光", "眼底", "青光"],
  },
  {
    id: "dental",
    label: "口腔",
    symbol: "口",
    aliases: ["牙疼", "拔牙", "矫正", "种植"],
    keywords: ["口腔", "牙", "正畸", "种植"],
  },
  {
    id: "ent",
    label: "耳鼻喉",
    symbol: "耳",
    aliases: ["鼻炎", "耳鸣", "嗓子疼"],
    keywords: ["耳", "鼻", "咽", "喉", "听力"],
  },
  {
    id: "psych",
    label: "精神心理",
    symbol: "心",
    aliases: ["失眠", "焦虑", "抑郁", "睡眠"],
    keywords: ["精神", "心理", "睡眠", "心身"],
  },
  {
    id: "other",
    label: "其他专科",
    symbol: "其",
    aliases: ["介入", "疼痛", "麻醉", "营养", "检验", "病理", "特需", "护理"],
    keywords: ["介入", "疼痛", "麻醉", "营养", "放射", "超声", "病理", "药学", "核医学", "全科", "检验", "护理", "体检", "干细胞", "特需"],
  },
];

const SOURCE_LABELS = {
  public_hospital_schedule_page: "医院官网公开表",
  public_hospital_schedule_api: "医院官网公开接口",
  public_hospital_weekly_table: "医院官网周排班",
};

const state = {
  city: "北京",
  district: "all",
  referenceLocationId: "none",
  query: "",
  date: "all",
  slot: "all",
  selectedDepartment: "all",
  selectedSubDepartment: "all",
  officialOnly: true,
  withScheduleOnly: false,
  sort: "default",
  hospitals: buildHospitalRegistry("北京"),
  schedules: [],
  schedulesByCity: {},
  selectedHospitalId: null,
  compareMode: false,
  compareHospitals: loadCompareHospitals(),
  compareReturnHospitalId: null,
};

const el = {};

document.addEventListener("DOMContentLoaded", async () => {
  cacheElements();
  populateCityFilter();
  populateDistrictFilter();
  populateLocationFilter();
  bindEvents();
  renderDepartments();
  renderEmptyDetail();
  await loadData();
  render();
});

function cacheElements() {
  [
    "sourceSummary",
    "metricHospitals",
    "metricSchedules",
    "workspace",
    "citySelect",
    "districtSelect",
    "locationInput",
    "locationOptions",
    "searchInput",
    "dateSelect",
    "resetFilters",
    "departmentNav",
    "activeDepartmentLabel",
    "officialOnly",
    "withScheduleOnly",
    "sortSelect",
    "hospitalList",
    "resultSummary",
    "detailContent",
  ].forEach((id) => {
    el[id] = document.getElementById(id);
  });
}

function bindEvents() {
  el.citySelect.addEventListener("change", (event) => {
    applyCityChange(event.target.value);
  });

  el.districtSelect.addEventListener("change", (event) => {
    state.district = event.target.value;
    populateLocationFilter();
    state.selectedHospitalId = null;
    render();
  });

  el.locationInput.addEventListener("input", (event) => {
    const nextLocationId = resolveReferenceLocationInput(event.target.value);
    if (nextLocationId === state.referenceLocationId) return;
    state.referenceLocationId = nextLocationId;
    state.selectedHospitalId = null;
    render();
  });

  el.locationInput.addEventListener("change", (event) => {
    const nextLocationId = resolveReferenceLocationInput(event.target.value);
    state.referenceLocationId = nextLocationId;
    el.locationInput.value = getLocationInputValueById(nextLocationId);
    state.selectedHospitalId = null;
    render();
  });

  el.searchInput.addEventListener("input", (event) => {
    state.query = event.target.value.trim();
    render();
  });

  el.dateSelect.addEventListener("change", (event) => {
    state.date = event.target.value;
    render();
  });

  document.querySelectorAll(".segment").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".segment").forEach((item) => item.classList.remove("is-active"));
      button.classList.add("is-active");
      state.slot = button.dataset.slot;
      render();
    });
  });

  el.officialOnly.addEventListener("change", (event) => {
    state.officialOnly = event.target.checked;
    render();
  });

  el.withScheduleOnly.addEventListener("change", (event) => {
    state.withScheduleOnly = event.target.checked;
    render();
  });

  el.sortSelect.addEventListener("change", (event) => {
    state.sort = event.target.value;
    render();
  });

  el.resetFilters.addEventListener("click", resetFilters);

  document.addEventListener("click", handleDocumentClick);
}

async function loadData() {
  try {
    const embeddedData = window.PROTOTYPE_RAW_DATA;

    if (typeof window.ALL_CITY_SCHEDULE_DATA === "undefined") {
      console.warn("all-city-schedule-data.js 未加载或尚未就绪，全城自动发现排班数据不可用");
    }

    const [bch, puh3, pumch] = embeddedData
      ? [embeddedData.bch, embeddedData.puh3, embeddedData.pumch]
      : await Promise.all([
          fetchJson(DATA_FILES.bch),
          fetchJson(DATA_FILES.puh3),
          fetchJson(DATA_FILES.pumch),
        ]);

    const normalizedSchedules = [
      ...normalizeBch(bch.records || []),
      ...normalizePuh3(puh3.records || []),
      ...normalizePumch(pumch.sampleRows || [], pumch.dateColumns || []),
    ];
    const discoveredSchedulesByCity = getDiscoveredSchedulesByCity();
    const currentSchedules = normalizedSchedules.filter((schedule) => isCurrentOrFutureSchedule(schedule));
    state.schedulesByCity = {
      北京: [...currentSchedules, ...(discoveredSchedulesByCity["北京"] || [])],
      上海: discoveredSchedulesByCity["上海"] || [],
      深圳: discoveredSchedulesByCity["深圳"] || [],
      杭州: discoveredSchedulesByCity["杭州"] || [],
    };
    state.schedules = getSchedulesForCity(state.city);

    populateDateFilter();
    state.selectedHospitalId = getFilteredHospitals()[0]?.id || null;
    updateSourceSummary(normalizedSchedules.length - currentSchedules.length);
  } catch (error) {
    console.error(error);
    state.schedulesByCity = { 北京: [], 上海: [], 深圳: [], 杭州: [] };
    state.schedules = getSchedulesForCity(state.city);
    populateDateFilter();
    updateSourceSummary(0, "样本载入失败：请用本地服务打开，或检查 prototype-data.js");
    el.hospitalList.innerHTML = `<div class="empty-state">样本数据暂时无法载入</div>`;
  }
}

function getSchedulesForCity(city) {
  return state.schedulesByCity[city] || [];
}

function getDiscoveredSchedulesByCity() {
  const recordsByCity = typeof window !== "undefined" ? window.ALL_CITY_SCHEDULE_DATA?.recordsByCity : null;
  if (!recordsByCity || typeof recordsByCity !== "object") return {};
  return Object.fromEntries(Object.entries(recordsByCity).map(([city, records]) => [
    city,
    Array.isArray(records) ? records.map((record, index) => normalizeDiscoveredSchedule(record, index)) : [],
  ]));
}

function normalizeDiscoveredSchedule(record, index) {
  const departmentName = record.departmentName || record.subDepartment || "未标注科室";
  return {
    id: record.id || `${record.hospitalId || "discovered"}-${index}`,
    hospitalId: record.hospitalId || "",
    hospitalName: record.hospitalName || "",
    campusName: record.campusName || record.hospitalName || "",
    departmentName,
    standardDepartment: record.standardDepartment || inferDepartment(departmentName),
    subDepartment: record.subDepartment || departmentName,
    doctorName: record.doctorName || "待定医生",
    doctorSpecial: record.doctorSpecial || "",
    professionalTitle: record.professionalTitle || "",
    clinicLevel: record.clinicLevel || "",
    visitDate: record.visitDate || "",
    dateLabel: record.dateLabel || record.displayDate || "",
    weekday: record.weekday || "",
    displayDate: record.displayDate || formatDateWithWeekday(record.visitDate || "", record.weekday || "", record.dateLabel || ""),
    timeSlot: record.timeSlot || "未标注",
    timeRange: record.timeRange || "",
    status: record.status || "公开排班",
    stopped: Boolean(record.stopped) || /停诊/.test(record.status || ""),
    price: record.price || "",
    capacityHint: record.capacityHint || "",
    sourceType: record.sourceType || "public_hospital_schedule_discovered",
    sourceUrl: record.sourceUrl || "",
    dataLevel: record.dataLevel || "L1",
    notes: record.notes || "官网公开排班，不代表实时可挂",
  };
}

function applyCityChange(nextCity) {
  if (!nextCity || nextCity === state.city) return;
  state.city = nextCity;
  state.hospitals = buildHospitalRegistry(state.city);
  state.schedules = getSchedulesForCity(state.city);
  state.district = "all";
  state.referenceLocationId = "none";
  state.query = "";
  state.date = "all";
  state.slot = "all";
  state.selectedDepartment = "all";
  state.selectedSubDepartment = "all";
  state.officialOnly = true;
  state.withScheduleOnly = false;
  state.sort = "default";
  state.selectedHospitalId = null;
  state.compareMode = false;
  state.compareHospitals = [];
  state.compareReturnHospitalId = null;

  populateDistrictFilter();
  populateLocationFilter();
  populateDateFilter();
  syncFilterControls();
  updateSourceSummary(0);
  render();
}

function updateSourceSummary(staleCount = 0, overrideText = "") {
  if (overrideText) {
    el.sourceSummary.textContent = overrideText;
    return;
  }
  const scheduledHospitalCount = unique(state.schedules.map((schedule) => schedule.hospitalId)).length;
  const refreshReport = getLatestRefreshReport();
  const refreshLabel = refreshReport?.generatedAt ? `，自动刷新于 ${formatReportTimestamp(refreshReport.generatedAt)}` : "";
  let schedulePolicy = getCityData(state.city).meta?.schedulePolicy || "当前城市未接入实时余号数据。";
  if (scheduledHospitalCount > 0 && /未接入公开排班样本/.test(schedulePolicy)) {
    schedulePolicy = `${state.city}已通过自动发现接入部分官网公开排班样本；公开排班不代表实时余号。`;
  }
  const baseText = `已纳入 ${state.hospitals.length} 家${state.city}医院官方/权威入口，${scheduledHospitalCount} 家有当前/未来公开排班`;
  el.sourceSummary.textContent = staleCount > 0
    ? `${baseText}，已过滤 ${staleCount} 条过期样本${refreshLabel}。${schedulePolicy}`
    : `${baseText}${refreshLabel}。${schedulePolicy}`;
}

function buildHospitalRegistry(city = "北京") {
  const registry = Array.isArray(getCityData(city).hospitals) ? getCityData(city).hospitals : [];
  const hospitalsById = new Map();

  registry.forEach((hospital) => {
    hospitalsById.set(hospital.id, {
      dataLevel: "L0",
      registryConfidence: "medium",
      entries: [],
      ...hospital,
      entries: hospital.entries || [],
    });
  });

  if (city === "北京") {
    L1_SCHEDULE_SAMPLES.forEach((hospital) => {
      const base = hospitalsById.get(hospital.id);
      hospitalsById.set(hospital.id, {
        ...(base || {}),
        ...hospital,
        name: base?.name || hospital.name,
        entries: mergeEntries(base?.entries || [], hospital.entries || []),
        registryConfidence: base?.registryConfidence || "high",
        dataLevel: "L1",
      });
    });
  }

  const wechatEntries = getWechatEntryMap(city);
  hospitalsById.forEach((hospital, id) => {
    const entries = wechatEntries[id] || [buildWechatDiscoveryEntry(hospital)];
    hospitalsById.set(id, {
      ...hospital,
      entries: mergeEntries(hospital.entries || [], entries),
    });
  });

  return [...hospitalsById.values()].sort((a, b) => {
    const districtScore = String(a.district || "").localeCompare(String(b.district || ""), "zh-Hans-CN");
    if (districtScore !== 0) return districtScore;
    return String(a.name || "").localeCompare(String(b.name || ""), "zh-Hans-CN");
  });
}

function getCityData(city = state.city) {
  const fallback = {
    hospitals: typeof window !== "undefined" && Array.isArray(window.BEIJING_3A_HOSPITALS) ? window.BEIJING_3A_HOSPITALS : [],
    wechatEntries: typeof window !== "undefined" && window.BEIJING_WECHAT_ENTRIES ? window.BEIJING_WECHAT_ENTRIES : {},
    referenceLocations: typeof window !== "undefined" && Array.isArray(window.BEIJING_REFERENCE_LOCATIONS) ? window.BEIJING_REFERENCE_LOCATIONS : [],
    hospitalCoordinates: typeof window !== "undefined" && window.BEIJING_HOSPITAL_COORDINATES ? window.BEIJING_HOSPITAL_COORDINATES : {},
    meta: { schedulePolicy: "北京保留已接入的少量公开排班样本。" },
  };
  if (typeof window === "undefined" || !window.CITY_DATA) return fallback;
  return window.CITY_DATA[city] || window.CITY_DATA["北京"] || fallback;
}

function getAvailableCities() {
  if (typeof window === "undefined" || !window.CITY_DATA) return ["北京"];
  return Object.keys(window.CITY_DATA);
}

function getWechatEntryMap(city = state.city) {
  return getCityData(city).wechatEntries || {};
}

function buildWechatDiscoveryEntry(hospital) {
  const officialSite = (hospital.entries || []).find((entry) => entry.type === "web" && entry.url)?.url || "";
  return {
    type: "wechat",
    name: "公众号入口待抓取",
    accountName: `${hospital.shortName || hospital.name} 官方公众号待核验`,
    accountType: "unknown",
    canRegister: "unknown",
    sourceUrl: officialSite,
    status: "discovery_pending",
    confidence: "low",
    notes: "等待从医院官网公开二维码或微信入口中抓取核验。",
  };
}

function mergeEntries(...entryLists) {
  const seen = new Set();
  return entryLists.flat().filter((entry) => {
    const key = [
      entry.type,
      entry.name,
      entry.url || entry.profileUrl || entry.sourceUrl || entry.value || entry.accountName || "",
    ].join("|");
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function populateCityFilter() {
  const cities = getAvailableCities();
  el.citySelect.innerHTML = cities.map((city) => `
    <option value="${escapeAttribute(city)}">${escapeHtml(city)}</option>
  `).join("");
  el.citySelect.value = cities.includes(state.city) ? state.city : "北京";
  state.city = el.citySelect.value;
}

function populateDistrictFilter() {
  const currentValue = state.district;
  const districts = unique(state.hospitals.map((hospital) => hospital.district)).sort((a, b) => a.localeCompare(b, "zh-Hans-CN"));
  el.districtSelect.innerHTML = `
    <option value="all">全城</option>
    ${districts.map((district) => `<option value="${escapeAttribute(district)}">${escapeHtml(district)}</option>`).join("")}
  `;
  el.districtSelect.value = districts.includes(currentValue) ? currentValue : "all";
  state.district = el.districtSelect.value;
}

function populateLocationFilter() {
  const scopedPoints = getScopedReferenceLocations();
  el.locationOptions.innerHTML = scopedPoints.map((point) => `
    <option value="${escapeAttribute(getLocationInputValue(point))}"></option>
  `).join("");

  if (!scopedPoints.some((point) => point.id === state.referenceLocationId)) {
    state.referenceLocationId = "none";
  }
  el.locationInput.value = getLocationInputValueById(state.referenceLocationId);
}

function getScopedReferenceLocations() {
  const points = getReferenceLocations();
  return state.district === "all"
    ? points
    : points.filter((point) => point.district === state.district);
}

function getLocationInputValue(point) {
  return point ? `${point.district} · ${point.name}` : "";
}

function getLocationInputValueById(locationId) {
  if (locationId === "none") return "";
  return getLocationInputValue(getReferenceLocations().find((point) => point.id === locationId));
}

function resolveReferenceLocationInput(value) {
  const query = value.trim();
  if (!query) return "none";
  const scopedPoints = getScopedReferenceLocations();
  const exact = scopedPoints.find((point) => getLocationInputValue(point) === query || point.name === query);
  if (exact) return exact.id;
  const fuzzyMatches = scopedPoints.filter((point) => getLocationInputValue(point).includes(query) || point.name.includes(query));
  return fuzzyMatches.length === 1 ? fuzzyMatches[0].id : "none";
}

function getReferenceLocations() {
  return getCityData(state.city).referenceLocations || [];
}

function getHospitalCoordinate(hospital) {
  return (getCityData(state.city).hospitalCoordinates || {})[hospital.id] || null;
}

function getSelectedReferenceLocation() {
  if (state.referenceLocationId === "none") return null;
  return getReferenceLocations().find((point) => point.id === state.referenceLocationId) || null;
}

function getLatestRefreshReport() {
  return typeof window !== "undefined" && window.PROTOTYPE_LATEST_REPORT
    ? window.PROTOTYPE_LATEST_REPORT
    : null;
}

function formatReportTimestamp(value) {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  return date.toLocaleString("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
}

async function fetchJson(url) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch(url, { signal: controller.signal });
    if (!response.ok) {
      throw new Error(`${url} ${response.status}`);
    }
    return response.json();
  } finally {
    clearTimeout(timeout);
  }
}

function normalizeBch(records) {
  return records.map((record, index) => {
    const visitDate = parseBchDate(record);
    return {
      id: `bch-${index}`,
      hospitalId: "bch",
      hospitalName: record.hospitalName,
      campusName: "本部",
      departmentName: record.departmentName,
      standardDepartment: inferDepartment(record.departmentName),
      subDepartment: record.departmentName || "未标注科室",
      doctorName: record.doctorName || "待定医生",
      doctorSpecial: "",
      professionalTitle: record.professionalTitle || "",
      clinicLevel: record.clinicLevel || "",
      visitDate,
      dateLabel: record.dateLabel || visitDate,
      weekday: extractWeekday(record.dateLabel),
      displayDate: formatDateWithWeekday(visitDate, extractWeekday(record.dateLabel), record.dateLabel),
      timeSlot: record.timeSlot || "未标注",
      timeRange: "",
      status: record.appointmentState || "未标注",
      stopped: /停诊/.test(record.appointmentState || ""),
      price: "",
      capacityHint: "",
      sourceType: record.sourceType || "public_hospital_schedule_page",
      sourceUrl: record.sourceUrl,
      dataLevel: "L1",
      notes: "公开出诊安排，不代表实时可挂",
    };
  });
}

function normalizePuh3(records) {
  return records.map((record, index) => ({
    id: `puh3-${index}`,
    hospitalId: "puh3",
    hospitalName: record.hospitalName,
    campusName: record.campusName || "北京大学第三医院本部",
    departmentName: record.departmentName,
    standardDepartment: inferDepartment(record.departmentName),
    subDepartment: record.departmentName || "未标注科室",
    doctorName: record.doctorName || "待定医生",
    doctorSpecial: record.doctorSpecial || record.groupName || "",
    professionalTitle: record.professionalTitle || "",
    clinicLevel: record.clinicLevel || "",
    visitDate: record.visitDate || "",
    dateLabel: record.visitDateLabel || record.visitDate || "",
    weekday: record.weekday || "",
    displayDate: formatDateWithWeekday(record.visitDate || "", record.weekday || "", record.visitDateLabel || ""),
    timeSlot: record.timeSlot || "未标注",
    timeRange: "",
    status: record.appointmentState || "未标注",
    stopped: record.stopFlag === "1" || /停诊/.test(record.appointmentState || ""),
    price: record.priceCnyRaw ? `${record.priceCnyRaw}元` : "",
    capacityHint: record.clinicLimitCountRaw ? `限号线索 ${record.clinicLimitCountRaw}` : "",
    sourceType: record.sourceType || "public_hospital_schedule_api",
    sourceUrl: record.sourceUrl,
    dataLevel: "L1",
    notes: "门诊限号线索不能等同于剩余号源",
  }));
}

function normalizePumch(sampleRows, dateColumns = []) {
  const schedules = [];
  let currentDepartment = "";

  sampleRows.forEach((row, rowIndex) => {
    let timeSlot = "";
    let startIndex = 1;

    if (["上午", "下午", "晚上", "夜间"].includes(row[0])) {
      timeSlot = row[0];
      startIndex = 1;
    } else {
      currentDepartment = row[0] || currentDepartment;
      timeSlot = row[1] || "未标注";
      startIndex = 2;
    }

    row.slice(startIndex).forEach((doctorText, dayIndex) => {
      if (!doctorText || doctorText === "—") return;
      const dateColumn = dateColumns[dayIndex] || {};
      doctorText
        .split(/\s+/)
        .filter(Boolean)
        .forEach((doctorName, doctorIndex) => {
          schedules.push({
            id: `pumch-${rowIndex}-${dayIndex}-${doctorIndex}`,
            hospitalId: "pumch",
            hospitalName: "北京协和医院",
            campusName: "东单院区",
            departmentName: currentDepartment,
            standardDepartment: inferDepartment(currentDepartment),
            subDepartment: currentDepartment || "未标注科室",
            doctorName,
            doctorSpecial: "",
            professionalTitle: "",
            clinicLevel: "普通门诊",
            visitDate: dateColumn.date || "",
            dateLabel: dateColumn.label || "",
            weekday: dateColumn.weekday || "",
            displayDate: formatDateWithWeekday(dateColumn.date || "", dateColumn.weekday || "", dateColumn.label || ""),
            timeSlot,
            timeRange: "",
            status: "公开排班",
            stopped: false,
            price: "",
            capacityHint: "",
            sourceType: "public_hospital_weekly_table",
            sourceUrl: "https://www.pumch.cn/dsearchs/dockervisit/3/1.html",
            dataLevel: "L1",
            notes: "官网周排班抽样，不代表实时可挂",
          });
        });
    });
  });

  return schedules;
}

function isCurrentOrFutureSchedule(schedule) {
  if (!schedule.visitDate) return true;
  const today = formatIsoDate(new Date());
  return schedule.visitDate >= today;
}

function parseBchDate(record) {
  const year = String(record.scheduleRange?.start || "").match(/(\d{4})年/)?.[1] || "2026";
  const match = String(record.dateLabel || "").match(/(\d{2})-(\d{2})/);
  if (!match) return "";
  return `${year}-${match[1]}-${match[2]}`;
}

function extractWeekday(value = "") {
  return String(value).match(/星期[一二三四五六日天]/)?.[0] || "";
}

function formatDateWithWeekday(isoDate = "", weekday = "", fallback = "") {
  const normalizedWeekday = normalizeWeekday(weekday || fallback);
  if (isoDate) {
    return [isoDate, normalizedWeekday].filter(Boolean).join(" ");
  }
  return [fallback, normalizedWeekday].filter(Boolean).join(" ") || "日期未公开";
}

function normalizeWeekday(value = "") {
  const text = String(value);
  if (/星期[一二三四五六日天]/.test(text)) {
    return text.match(/星期[一二三四五六日天]/)[0].replace("星期天", "星期日");
  }
  const match = text.match(/周[一二三四五六日天]/);
  if (!match) return "";
  const day = match[0].replace("周", "").replace("天", "日");
  return `星期${day}`;
}

function addDays(date, days) {
  const next = new Date(date);
  next.setDate(next.getDate() + days);
  return next;
}

function formatIsoDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function populateDateFilter() {
  const currentValue = state.date;
  const dated = unique(state.schedules.map((schedule) => schedule.visitDate).filter(Boolean))
    .sort((a, b) => Date.parse(a) - Date.parse(b));
  el.dateSelect.innerHTML = `
    <option value="all">全部日期</option>
    <option value="weekend">只看周末</option>
    ${dated.map((date) => {
      const sample = state.schedules.find((schedule) => schedule.visitDate === date);
      const label = formatDateWithWeekday(date, sample?.weekday || sample?.dateLabel || "");
      return `<option value="date:${escapeAttribute(date)}">${escapeHtml(label)}</option>`;
    }).join("")}
  `;
  el.dateSelect.value = [...el.dateSelect.options].some((option) => option.value === currentValue) ? currentValue : "all";
  state.date = el.dateSelect.value;
}

function inferDepartment(name = "") {
  const target = String(name);
  const found = DEPARTMENTS.find((department) => {
    if (department.id === "all") return false;
    return department.keywords.some((keyword) => target.includes(keyword));
  });
  return found?.id || "all";
}

function render() {
  renderDepartments();
  const hospitals = getFilteredHospitals();
  const selectedExists = hospitals.some((hospital) => hospital.id === state.selectedHospitalId);
  if (!selectedExists) {
    state.selectedHospitalId = hospitals[0]?.id || null;
  }

  renderMetrics(hospitals);
  renderHospitals(hospitals);
  renderDetail();
}

function renderMetrics(hospitals) {
  const scheduleCount = hospitals.reduce((sum, hospital) => sum + hospital.filteredSchedules.length, 0);
  el.metricHospitals.textContent = hospitals.length;
  el.metricSchedules.textContent = scheduleCount;
  el.resultSummary.textContent = `${hospitals.length} 家匹配，${scheduleCount} 条公开排班`;
  el.workspace.classList.toggle("is-compare-mode", state.compareMode);
}

function renderDepartments() {
  const counts = getDepartmentCounts();
  const active = DEPARTMENTS.find((item) => item.id === state.selectedDepartment);
  el.activeDepartmentLabel.textContent = state.selectedSubDepartment === "all"
    ? active?.label || "全部"
    : state.selectedSubDepartment;

  el.departmentNav.innerHTML = DEPARTMENTS.map((department) => {
    const aliases = department.aliases.slice(0, 3).join(" / ") || "全部公开排班";
    const count = counts[department.id] || 0;
    const isActive = department.id === state.selectedDepartment;
    const subDepartments = isActive ? getSubDepartmentsForPrimary(department.id).slice(0, 14) : [];
    return `
      <div class="department-group">
        <button class="department-button ${isActive ? "is-active" : ""}" data-department="${department.id}" type="button">
          <span class="dept-symbol">${department.symbol}</span>
          <span>
            <strong>${department.label}</strong>
            <small>${escapeHtml(aliases)}</small>
          </span>
          <em>${count}</em>
        </button>
        ${subDepartments.length ? `
          <div class="subdept-list">
            <button class="subdept-button ${state.selectedSubDepartment === "all" ? "is-active" : ""}" data-subdepartment="all" type="button">
              <span>全部${escapeHtml(department.label)}</span>
              <em>${count}</em>
            </button>
            ${subDepartments.map((item) => `
              <button class="subdept-button ${state.selectedSubDepartment === item.name ? "is-active" : ""}" data-subdepartment="${escapeAttribute(item.name)}" type="button">
                <span>${escapeHtml(item.name)}</span>
                <em>${item.count}</em>
              </button>
            `).join("")}
          </div>
        ` : ""}
      </div>
    `;
  }).join("");
}

function getDepartmentCounts() {
  const counts = Object.fromEntries(DEPARTMENTS.map((department) => [department.id, 0]));
  state.schedules.forEach((schedule) => {
    counts.all += 1;
    if (schedule.standardDepartment !== "all" && counts[schedule.standardDepartment] !== undefined) {
      counts[schedule.standardDepartment] += 1;
    }
  });
  return counts;
}

function getSubDepartmentsForPrimary(primaryId) {
  if (primaryId === "all") return [];
  const counts = new Map();
  state.schedules.forEach((schedule) => {
    if (schedule.standardDepartment !== primaryId) return;
    const name = schedule.subDepartment || schedule.departmentName || "未标注科室";
    counts.set(name, (counts.get(name) || 0) + 1);
  });
  // Also surface department aliases so users can filter by known sub-specialties
  // even when no schedule data is currently loaded for them.
  const department = DEPARTMENTS.find((item) => item.id === primaryId);
  if (department) {
    department.aliases.forEach((alias) => {
      if (!counts.has(alias)) {
        counts.set(alias, 0);
      }
    });
  }
  return [...counts.entries()]
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name, "zh-Hans-CN"));
}

function renderHospitals(hospitals) {
  if (!hospitals.length) {
    el.hospitalList.innerHTML = `<div class="empty-state">暂无匹配医院</div>`;
    return;
  }

  el.hospitalList.innerHTML = hospitals.map((hospital) => {
    const departments = unique(hospital.filteredSchedules.map((item) => item.departmentName)).slice(0, 5);
    const dateRange = getDateRangeLabel(hospital.filteredSchedules);
    const activeClass = hospital.id === state.selectedHospitalId ? "is-active" : "";
    const entryCount = getEntries(hospital).length;
    const dataLevel = getHospitalDataLevel(hospital);
    const dataLabel = dataLevel === "L1" ? "L1 公开出诊" : "L0 入口";
    const scheduleLabel = hospital.filteredSchedules.length
      ? `公开出诊 ${hospital.filteredSchedules.length}`
      : "暂未接入排班";
    return `
      <button class="hospital-card ${activeClass}" data-hospital="${hospital.id}" type="button">
        <div class="hospital-title">
          <div>
            <h3>${escapeHtml(hospital.name)}</h3>
            <p>${escapeHtml(hospital.campusName)} · ${escapeHtml(hospital.district)} · ${escapeHtml(hospital.level)}</p>
          </div>
          <span class="badge ${dataLevel === "L1" ? "public" : "l0"}">${dataLabel}</span>
        </div>
        <div class="badge-row">
          <span class="badge">入口 ${entryCount}</span>
          <span class="badge ${hospital.filteredSchedules.length ? "public" : "warn"}">${scheduleLabel}</span>
          <span class="badge warn">需官方确认</span>
          ${getEntries(hospital).some((entry) => entry.type === "mini") ? `<span class="badge coral">含小程序</span>` : ""}
          ${getEntries(hospital).some((entry) => entry.type === "wechat") ? `<span class="badge public">含公众号</span>` : ""}
        </div>
        <div class="hospital-meta">
          <span class="meta-cell"><strong>${formatDistance(getDistanceValue(hospital))}</strong>${escapeHtml(getDistanceLabel())}</span>
          <span class="meta-cell"><strong>${escapeHtml(dateRange)}</strong>公开日期</span>
          <span class="meta-cell"><strong>${escapeHtml(hospital.type)}</strong>医院类型</span>
        </div>
        <div class="dept-list">${escapeHtml(departments.join("、") || "暂无排班样本，可通过官方入口确认科室/号源")}</div>
        <div class="quick-actions">
          <span class="mini-action ${state.compareHospitals.includes(hospital.id) ? "primary" : ""}" data-action="add-hospital" data-hospital="${hospital.id}">
            ${state.compareHospitals.includes(hospital.id) ? "已加入对比" : "加入对比"}
          </span>
        </div>
      </button>
    `;
  }).join("");
}

function renderDetail() {
  try {
    if (!state.selectedHospitalId) {
      renderEmptyDetail();
      return;
    }

    const hospital = getFilteredHospitals().find((item) => item.id === state.selectedHospitalId)
      || state.hospitals.find((item) => item.id === state.selectedHospitalId);

    if (!hospital) {
      renderEmptyDetail();
      return;
    }

    const schedules = hospital.filteredSchedules || getSchedulesForHospital(hospital.id);
    const entries = getEntries(hospital);
    const tableRows = schedules.slice(0, 80);
    const dataLevel = getHospitalDataLevel({ ...hospital, filteredSchedules: schedules });

    el.detailContent.innerHTML = `
      <div class="detail-header">
        <div class="detail-header-top">
          <div>
            <div class="detail-title-row">
              <h2>${escapeHtml(hospital.name)}</h2>
              ${state.compareMode ? "" : `
                <button class="mini-action" data-action="toggle-compare-mode" data-hospital="${hospital.id}" type="button">对比模式</button>
              `}
            </div>
            <p>${escapeHtml(hospital.campusName)} · ${escapeHtml(hospital.address)}</p>
          </div>
          <span class="badge ${dataLevel === "L1" ? "warn" : "l0"}">${dataLevel === "L1" ? "公开排班非实时余号" : "仅入口导航，排班待接入"}</span>
        </div>
      </div>

      ${state.compareMode ? renderCompareMode() : `
        <section class="detail-section">
          <h3>挂号信息</h3>
          <div class="entry-grid compact-entry-grid">
            ${renderCoreEntryModules(entries)}
          </div>
        </section>

        <section class="detail-section">
          <div class="table-toolbar">
            <div>
              <h3>号源信息（公开排班）</h3>
              <p>${schedules.length} 条匹配；列表最多展示前 80 条</p>
            </div>
            <button class="mini-action" data-action="add-hospital" data-hospital="${hospital.id}" type="button">
              ${state.compareHospitals.includes(hospital.id) ? "已加入对比" : "加入对比"}
            </button>
          </div>
          ${renderScheduleTable(tableRows)}
        </section>
      `}
    `;
  } catch (renderError) {
    console.error("renderDetail 失败", renderError);
    showToast("详情加载失败，请刷新重试");
    renderEmptyDetail();
  }
}

function renderCompareMode() {
  const hospitals = getCompareHospitals();
  return `
    <section class="detail-section">
      <div class="table-toolbar">
        <div>
          <h3>号源对比</h3>
          <p>对比医院列来自医院列表的“加入对比”；当前展示 ${hospitals.length} 家。</p>
        </div>
        <div class="compare-toolbar-actions">
          <button class="mini-action" data-action="clear-compare" type="button">清空对比</button>
          <button class="mini-action primary" data-action="exit-compare-mode" type="button">退出对比模式</button>
        </div>
      </div>
      ${hospitals.length ? `
        <div class="compare-grid">
          ${hospitals.map((hospital) => renderCompareColumn(hospital)).join("")}
        </div>
      ` : `<div class="empty-state">当前没有对比医院，可以退出对比模式后重新加入。</div>`}
    </section>
  `;
}

function renderScheduleTable(rows) {
  if (!rows.length) {
    return `<div class="empty-state">当前筛选下暂无公开排班；已保留官方入口，实际余号和可约日期需跳转确认。</div>`;
  }

  return `
    <div class="schedule-table-wrap">
      <table>
        <thead>
          <tr>
            <th>日期</th>
            <th>时段</th>
            <th>具体时间</th>
            <th>科室</th>
            <th>医生</th>
            <th>状态</th>
            <th>线索</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          ${rows.map((row) => `
            <tr>
              <td>${escapeHtml(row.displayDate || formatDateWithWeekday(row.visitDate, row.weekday, row.dateLabel))}</td>
              <td>${escapeHtml(row.timeSlot)}</td>
              <td>${escapeHtml(row.timeRange || "未公开")}</td>
              <td>${escapeHtml(row.departmentName)}</td>
              <td class="doctor-cell">
                <strong>${escapeHtml(row.doctorName)}</strong>
                <span>${escapeHtml([row.professionalTitle, row.clinicLevel, row.doctorSpecial].filter(Boolean).join(" · "))}</span>
              </td>
              <td>${renderStatus(row)}</td>
              <td>${escapeHtml(row.capacityHint || row.price || "需官方确认")}</td>
              <td>
                <button class="mini-action" data-action="add-schedule" data-schedule="${row.id}" type="button">加入</button>
              </td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function renderStatus(row) {
  if (row.stopped) {
    return `<span class="status-pill stop">停诊</span>`;
  }
  if (/未停诊/.test(row.status)) {
    return `<span class="status-pill ok">未停诊</span>`;
  }
  return `<span class="status-pill neutral">${escapeHtml(row.status || "公开排班")}</span>`;
}

function renderCoreEntryModules(entries) {
  const officialSite = entries.find((entry) => entry.type === "web" && entry.url);
  const wechatEntries = entries.filter((entry) => entry.type === "wechat" || entry.type === "mini");
  return [
    renderOfficialSiteModule(officialSite),
    renderWechatModule(wechatEntries),
  ].filter(Boolean).join("");
}

function renderOfficialSiteModule(entry) {
  if (!entry) {
    return `
      <div class="entry-row action-entry official-entry no-entry-visual">
        <div class="entry-compact-main">
          <strong>挂号官网待补充</strong>
          <span>官方挂号入口尚未核验</span>
        </div>
        <div class="entry-actions">
          <span class="link-button disabled" aria-disabled="true">待补充</span>
        </div>
      </div>
    `;
  }

  return `
    <div class="entry-row action-entry official-entry no-entry-visual">
      <div class="entry-compact-main">
        <strong>挂号官网</strong>
        <span>${escapeHtml(entry.name || "医院官网")} · ${entry.status === "official" || entry.status === "official_entry" ? "官方入口" : "待核验"}</span>
        <code class="entry-key">${escapeHtml(entry.url)}</code>
      </div>
      <div class="entry-actions">
        <a class="link-button primary" href="${escapeAttribute(entry.url)}" target="_blank" rel="noreferrer">打开官网</a>
        <button class="link-button" data-action="copy" data-copy="${escapeAttribute(entry.url)}" type="button">复制网址</button>
      </div>
    </div>
  `;
}

function renderWechatModule(entries) {
  if (!entries.length) {
    return `
      <div class="entry-row action-entry wechat-entry grouped-wechat-entry no-entry-visual">
        <div class="entry-compact-main">
          <strong>微信入口待抓取</strong>
          <span>公众号/服务号/小程序二维码尚未核验</span>
        </div>
        <div class="entry-actions">
          <span class="link-button disabled" aria-disabled="true">待补充</span>
        </div>
      </div>
    `;
  }

  const primary = entries.find((entry) => entry.type === "wechat" && (entry.accountType === "service_account" || entry.canRegister === "yes" || entry.canRegister === "likely"))
    || entries.find((entry) => entry.type === "wechat")
    || entries[0];
  const openUrl = primary.profileUrl || primary.url || primary.sourceUrl || "";
  const sourceUrl = primary.sourceUrl || primary.url || "";
  const names = unique(entries.map((entry) => getWechatModuleName(entry)).filter(Boolean));
  const qrTiles = entries.map((entry) => renderWechatQrTile(entry)).filter(Boolean).join("");
  const hasQrTiles = Boolean(qrTiles);
  const sourceLine = sourceUrl
    ? `<a class="entry-source-link" href="${escapeAttribute(sourceUrl)}" target="_blank" rel="noreferrer">来源：${escapeHtml(sourceUrl)}</a>`
    : `<span class="entry-source-link muted">来源待抓取</span>`;

  return `
    <div class="entry-row action-entry grouped-wechat-entry${hasQrTiles ? "" : " no-entry-visual"}">
      ${hasQrTiles ? `<div class="wechat-tile-strip">${qrTiles}</div>` : ""}
      <div class="entry-compact-main">
        <strong>微信入口</strong>
        <span>公众号/服务号/小程序集中入口</span>
        <div class="wechat-name-list">
          ${names.map((name) => `<code class="entry-key">${escapeHtml(name)}</code>`).join("")}
        </div>
        ${sourceLine}
      </div>
      <div class="entry-actions">
        ${openUrl ? `<a class="link-button primary" href="${escapeAttribute(openUrl)}" target="_blank" rel="noreferrer">打开微信入口</a>` : `<span class="link-button disabled" aria-disabled="true">待补充</span>`}
        <button class="link-button" data-action="copy" data-copy="${escapeAttribute(names[0] || "微信入口")}" type="button">复制名称</button>
      </div>
    </div>
  `;
}

function renderWechatQrTile(entry) {
  const label = entry.type === "mini" ? "微信小程序" : getWechatVisualLabel(entry.accountType);
  const title = getWechatModuleName(entry) || label;
  const imageUrl = entry.qrImageUrl || (entry.qrPayload ? buildQrCodeUrl(entry.qrPayload) : "");
  if (!imageUrl) return "";
  return `
    <div class="wechat-tile">
      ${renderEntryVisual({
        label,
        title,
        imageUrl,
        zoomTitle: title,
        zoomSubtitle: label,
      })}
    </div>
  `;
}

function getWechatModuleName(entry) {
  return entry.accountName || entry.value || entry.name || "";
}

function renderEntryVisual({ label, title, imageUrl = "", zoomTitle = "", zoomSubtitle = "" }) {
  if (!imageUrl) return "";

  return `
    <div class="entry-visual-stack">
      <button class="entry-visual has-qr" data-action="zoom-qr" data-qr-src="${escapeAttribute(imageUrl)}" data-qr-title="${escapeAttribute(zoomTitle || title || label)}" data-qr-subtitle="${escapeAttribute(zoomSubtitle || label)}" type="button" title="点击放大${escapeAttribute(label)}">
        <img src="${escapeAttribute(imageUrl)}" alt="${escapeAttribute(title || label)}二维码" loading="lazy" />
      </button>
      <span>${escapeHtml(label)}</span>
    </div>
  `;
}

function getEntrySearchFields(entry) {
  return [
    entry.name,
    entry.url,
    entry.profileUrl,
    entry.sourceUrl,
    entry.value,
    entry.accountName,
    entry.notes,
  ];
}

function getWechatVisualLabel(type) {
  return {
    official_account: "微信公众号",
    service_account: "微信服务号",
    subscription_account: "微信订阅号",
    service_or_subscription: "微信服务号/订阅号",
    mini_program: "微信小程序",
  }[type] || "公众号入口";
}

function getWechatAccountTypeLabel(type) {
  return {
    official_account: "公众号",
    service_account: "服务号",
    subscription_account: "订阅号",
    service_or_subscription: "服务号/订阅号",
    mini_program: "小程序",
    unknown: "类型待核验",
  }[type] || "";
}

function getWechatRegisterLabel(value) {
  return {
    yes: "可挂号",
    likely: "疑似可挂号",
    unknown: "挂号能力待核验",
    no: "不可挂号",
  }[value] || "";
}

function buildQrCodeUrl(value) {
  return `https://api.qrserver.com/v1/create-qr-code/?size=96x96&margin=1&data=${encodeURIComponent(value)}`;
}

function renderEmptyDetail() {
  el.detailContent.innerHTML = `
    <div class="detail-empty">
      <div>
        <div class="empty-mark" aria-hidden="true"></div>
        <strong>请选择一家医院</strong>
        <p>医院详情、公开排班和官方入口会显示在这里。</p>
      </div>
    </div>
  `;
}

function getFilteredHospitals() {
  const hasScheduleFilters = state.date !== "all"
    || state.slot !== "all"
    || state.selectedDepartment !== "all"
    || state.selectedSubDepartment !== "all";

  const hospitals = state.hospitals
    .filter((hospital) => state.district === "all" || hospital.district === state.district)
    .map((hospital) => {
      const filteredSchedules = getSchedulesForHospital(hospital.id);
      const queryMatchesHospital = matchesText(hospital.name, state.query)
        || matchesText(hospital.shortName, state.query)
        || matchesText(hospital.district, state.query)
        || matchesText(hospital.type, state.query)
        || matchesText(hospital.address, state.query)
        || getEntries(hospital).some((entry) => getEntrySearchFields(entry).some((field) => matchesText(field, state.query)));
      const includeByQuery = !state.query || queryMatchesHospital || filteredSchedules.length > 0;
      const includeByScheduleFilter = !hasScheduleFilters || filteredSchedules.length > 0 || queryMatchesHospital;
      const includeByDataOnly = !state.withScheduleOnly || filteredSchedules.length > 0;
      return {
        ...hospital,
        filteredSchedules,
        includeByQuery,
        includeByScheduleFilter,
        includeByDataOnly,
      };
    })
    .filter((hospital) => hospital.includeByQuery && hospital.includeByScheduleFilter && hospital.includeByDataOnly);

  return sortHospitals(hospitals);
}

function getSchedulesForHospital(hospitalId) {
  return state.schedules.filter((schedule) => {
    if (schedule.hospitalId !== hospitalId) return false;
    if (state.slot !== "all" && schedule.timeSlot !== state.slot) return false;
    if (state.selectedDepartment !== "all" && schedule.standardDepartment !== state.selectedDepartment) return false;
    if (state.selectedSubDepartment !== "all" && !matchesAnyToken(schedule.subDepartment, state.selectedSubDepartment)) return false;
    if (state.date === "weekend" && !isWeekendSchedule(schedule)) return false;
    if (state.date.startsWith("date:") && schedule.visitDate !== state.date.slice(5)) return false;

    if (state.query) {
      const department = DEPARTMENTS.find((item) => item.id === schedule.standardDepartment);
      const exactFields = [
        schedule.hospitalName,
        schedule.campusName,
        schedule.doctorName,
        schedule.doctorSpecial,
        schedule.professionalTitle,
        schedule.clinicLevel,
      ];
      const aliasFields = [
        schedule.departmentName,
        department?.label,
        ...(department?.aliases || []),
      ];
      if (!exactFields.some((field) => matchesText(field, state.query))
        && !aliasFields.some((field) => matchesAnyToken(field, state.query))) {
        return false;
      }
    }

    return true;
  });
}

function sortHospitals(hospitals) {
  return hospitals.sort((a, b) => {
    if (state.sort === "distance" && getSelectedReferenceLocation()) {
      return getDistanceValue(a) - getDistanceValue(b);
    }
    if (state.sort === "scheduleCount") {
      return b.filteredSchedules.length - a.filteredSchedules.length;
    }
    if (state.sort === "recent") {
      return getLatestDateValue(b.filteredSchedules) - getLatestDateValue(a.filteredSchedules);
    }
    const scheduleScore = b.filteredSchedules.length - a.filteredSchedules.length;
    const entryScore = getEntries(b).length - getEntries(a).length;
    if (state.officialOnly && entryScore !== 0) return entryScore;
    if (scheduleScore !== 0) return scheduleScore;
    if (!state.officialOnly && entryScore !== 0) return entryScore;
    const levelScore = getHospitalDataLevel(b).localeCompare(getHospitalDataLevel(a));
    if (levelScore !== 0) return levelScore;
    if (getSelectedReferenceLocation()) return getDistanceValue(a) - getDistanceValue(b);
    return String(a.name || "").localeCompare(String(b.name || ""), "zh-Hans-CN");
  });
}

function isWeekendSchedule(schedule) {
  const text = `${schedule.weekday || ""}${schedule.dateLabel || ""}`;
  return /周六|周日|星期六|星期日|星期天/.test(text);
}

function getLatestDateValue(schedules) {
  const dates = schedules
    .map((item) => Date.parse(item.visitDate))
    .filter((value) => Number.isFinite(value));
  return dates.length ? Math.max(...dates) : 0;
}

function getDateRangeLabel(schedules) {
  const labels = unique(schedules.map((item) => item.visitDate || item.dateLabel).filter(Boolean));
  if (!labels.length) return "暂无公开排班";
  if (labels.length === 1) return labels[0];
  return `${labels[0]} 至 ${labels[labels.length - 1]}`;
}

function getEntries(hospital) {
  return mergeEntries(hospital.entries || [], COMMON_ENTRIES);
}

function getHospitalDataLevel(hospital) {
  if ((hospital.filteredSchedules || []).length > 0) return "L1";
  return hospital.dataLevel || "L0";
}

function getDistanceValue(hospital) {
  const reference = getSelectedReferenceLocation();
  const coordinate = getHospitalCoordinate(hospital);
  if (reference && coordinate) {
    return calculateDistanceKm(reference, coordinate);
  }
  return Number.POSITIVE_INFINITY;
}

function getDistanceLabel() {
  const reference = getSelectedReferenceLocation();
  return reference ? `距${reference.name}` : "选择位置后排序";
}

function formatDistance(distanceKm) {
  const value = Number(distanceKm);
  return Number.isFinite(value) ? `${value.toFixed(1)} km` : "待选择";
}

function calculateDistanceKm(from, to) {
  const earthRadiusKm = 6371;
  const lat1 = degreesToRadians(Number(from.lat));
  const lat2 = degreesToRadians(Number(to.lat));
  const deltaLat = degreesToRadians(Number(to.lat) - Number(from.lat));
  const deltaLng = degreesToRadians(Number(to.lng) - Number(from.lng));
  if (![lat1, lat2, deltaLat, deltaLng].every(Number.isFinite)) {
    return Number.POSITIVE_INFINITY;
  }
  const a = Math.sin(deltaLat / 2) ** 2
    + Math.cos(lat1) * Math.cos(lat2) * Math.sin(deltaLng / 2) ** 2;
  return earthRadiusKm * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

function degreesToRadians(value) {
  return value * Math.PI / 180;
}

function handleDocumentClick(event) {
  const subDepartmentButton = event.target.closest("[data-subdepartment]");
  if (subDepartmentButton) {
    state.selectedSubDepartment = subDepartmentButton.dataset.subdepartment;
    state.selectedHospitalId = null;
    render();
    return;
  }

  const departmentButton = event.target.closest("[data-department]");
  if (departmentButton) {
    state.selectedDepartment = departmentButton.dataset.department;
    state.selectedSubDepartment = "all";
    state.selectedHospitalId = null;
    render();
    return;
  }

  const hospitalButton = event.target.closest("[data-hospital]");
  const actionTarget = event.target.closest("[data-action]");

  if (hospitalButton && (!actionTarget || actionTarget.dataset.action === "view")) {
    state.selectedHospitalId = hospitalButton.dataset.hospital;
    render();
    return;
  }

  if (!actionTarget) return;

  const action = actionTarget.dataset.action;
  if (action === "add-hospital") {
    addHospitalToCompare(actionTarget.dataset.hospital);
  }
  if (action === "add-schedule") {
    addScheduleToCompare(actionTarget.dataset.schedule);
  }
  if (action === "remove-compare") {
    removeCompareHospital(actionTarget.dataset.hospital);
  }
  if (action === "clear-compare") {
    clearCompareToCurrentHospital();
  }
  if (action === "toggle-compare-mode") {
    toggleCompareMode(actionTarget.dataset.hospital);
  }
  if (action === "exit-compare-mode") {
    exitCompareMode();
  }
  if (action === "copy") {
    copyText(actionTarget.dataset.copy);
  }
  if (action === "zoom-qr") {
    openQrZoom(actionTarget.dataset.qrSrc, actionTarget.dataset.qrTitle, actionTarget.dataset.qrSubtitle);
  }
  if (action === "close-qr-zoom") {
    closeQrZoom();
  }
}

function openQrZoom(src, title, subtitle) {
  if (!src) return;
  let modal = document.getElementById("qrZoomModal");
  if (!modal) {
    modal = document.createElement("div");
    modal.id = "qrZoomModal";
    modal.className = "qr-zoom-modal";
    modal.hidden = true;
    document.body.appendChild(modal);
  }

  modal.innerHTML = `
    <div class="qr-zoom-backdrop" data-action="close-qr-zoom"></div>
    <div class="qr-zoom-dialog" role="dialog" aria-modal="true" aria-label="二维码放大预览">
      <button class="qr-zoom-close" data-action="close-qr-zoom" type="button" aria-label="关闭二维码预览">×</button>
      <img src="${escapeAttribute(src)}" alt="${escapeAttribute(title || "二维码")}" />
      <strong>${escapeHtml(title || "二维码")}</strong>
      ${subtitle ? `<span>${escapeHtml(subtitle)}</span>` : ""}
    </div>
  `;
  modal.hidden = false;
  document.body.classList.add("modal-open");
}

function closeQrZoom() {
  const modal = document.getElementById("qrZoomModal");
  if (!modal) return;
  modal.hidden = true;
  modal.innerHTML = "";
  document.body.classList.remove("modal-open");
}

function addHospitalToCompare(hospitalId) {
  const hospital = state.hospitals.find((item) => item.id === hospitalId);
  if (!hospital) return;
  if (!state.compareMode) {
    state.compareReturnHospitalId = state.selectedHospitalId || hospitalId;
  }
  if (!state.compareHospitals.includes(hospitalId)) {
    state.compareHospitals.push(hospitalId);
    state.compareHospitals = state.compareHospitals.slice(0, 4);
    saveCompareHospitals();
  }
  state.selectedHospitalId = hospitalId;
  state.compareMode = true;
  showToast("已加入号源对比");
  render();
}

function addScheduleToCompare(scheduleId) {
  const schedule = state.schedules.find((item) => item.id === scheduleId);
  if (!schedule) return;
  addHospitalToCompare(schedule.hospitalId);
}

function removeCompareHospital(hospitalId) {
  state.compareHospitals = state.compareHospitals.filter((id) => id !== hospitalId);
  if (state.selectedHospitalId === hospitalId) {
    state.selectedHospitalId = state.compareHospitals[0] || state.compareReturnHospitalId || null;
  }
  saveCompareHospitals();
  render();
}

function clearCompareToCurrentHospital() {
  const currentHospitalId = state.selectedHospitalId || state.compareHospitals[0] || state.compareReturnHospitalId;
  state.compareHospitals = currentHospitalId ? [currentHospitalId] : [];
  saveCompareHospitals();
  render();
}

function toggleCompareMode(hospitalId) {
  if (!state.compareMode) {
    state.compareReturnHospitalId = state.selectedHospitalId || hospitalId || null;
    const filtered = getFilteredHospitals().map((hospital) => hospital.id);
    const seedIds = unique([hospitalId, ...state.compareHospitals, ...filtered]).slice(0, 3);
    state.compareHospitals = seedIds;
    saveCompareHospitals();
    state.compareMode = true;
    render();
    return;
  }
  exitCompareMode();
}

function exitCompareMode() {
  state.compareMode = false;
  if (state.compareReturnHospitalId) {
    state.selectedHospitalId = state.compareReturnHospitalId;
  }
  state.compareReturnHospitalId = null;
  render();
}

function getCompareHospitals() {
  return state.compareHospitals
    .map((id) => state.hospitals.find((hospital) => hospital.id === id))
    .filter(Boolean)
    .map((hospital) => ({
      ...hospital,
      filteredSchedules: getSchedulesForHospital(hospital.id),
    }));
}

function renderCompareColumn(hospital) {
  const schedules = (hospital.filteredSchedules || []).slice(0, 8);
  const entries = getCoreCompareEntries(getEntries(hospital));
  return `
    <article class="compare-column">
      <div class="compare-column-head">
        <div class="detail-title-row">
          <h3>${escapeHtml(hospital.shortName)}</h3>
          <button class="mini-action" data-action="remove-compare" data-hospital="${hospital.id}" type="button">移除</button>
        </div>
        <p>${escapeHtml(hospital.campusName)} · ${escapeHtml(hospital.district)} · ${hospital.filteredSchedules.length} 条公开排班</p>
      </div>
      <div class="compare-column-body">
        ${entries.map((entry) => `
          <div class="compare-entry ${entry.kind === "wechat" ? "wechat-compare-entry" : ""}">
            <strong>${escapeHtml(entry.title)}</strong>
            <span>${escapeHtml(entry.value)}</span>
          </div>
        `).join("")}
        ${schedules.length ? schedules.map((schedule) => `
          <div class="compare-schedule">
            <strong>${escapeHtml(schedule.displayDate || formatDateWithWeekday(schedule.visitDate, schedule.weekday, schedule.dateLabel))} · ${escapeHtml(schedule.timeSlot)}</strong>
            <span>${escapeHtml(schedule.departmentName)} · ${escapeHtml(schedule.doctorName)} · ${escapeHtml(schedule.timeRange || "具体时间未公开")}</span>
          </div>
        `).join("") : `<div class="empty-state">当前筛选下暂无排班</div>`}
      </div>
    </article>
  `;
}

function getCoreCompareEntries(entries) {
  const officialSite = entries.find((entry) => entry.type === "web" && entry.url);
  const wechatEntries = entries.filter((entry) => entry.type === "wechat" || entry.type === "mini");
  const result = [];
  if (officialSite) {
    result.push({ kind: "web", title: "挂号官网", value: officialSite.url });
  }
  if (wechatEntries.length) {
    result.push({
      kind: "wechat",
      title: "微信入口",
      value: unique(wechatEntries.map((entry) => getWechatModuleName(entry)).filter(Boolean)).join(" / "),
    });
  }
  return result;
}

function loadCompareHospitals() {
  try {
    return JSON.parse(localStorage.getItem("registrationCompareHospitals") || "[]");
  } catch (e) {
    console.warn("localStorage compareHospitals 解析失败，已重置", e);
    localStorage.removeItem("registrationCompareHospitals");
    return [];
  }
}

function saveCompareHospitals() {
  localStorage.setItem("registrationCompareHospitals", JSON.stringify(state.compareHospitals));
}

function syncFilterControls() {
  el.citySelect.value = state.city;
  el.districtSelect.value = state.district;
  el.locationInput.value = getLocationInputValueById(state.referenceLocationId);
  el.searchInput.value = state.query;
  el.dateSelect.value = state.date;
  el.officialOnly.checked = state.officialOnly;
  el.withScheduleOnly.checked = state.withScheduleOnly;
  el.sortSelect.value = state.sort;
  document.querySelectorAll(".segment").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.slot === state.slot);
  });
}

function resetFilters() {
  state.district = "all";
  state.referenceLocationId = "none";
  state.query = "";
  state.date = "all";
  state.slot = "all";
  state.selectedDepartment = "all";
  state.selectedSubDepartment = "all";
  state.officialOnly = true;
  state.withScheduleOnly = false;
  state.sort = "default";
  state.selectedHospitalId = null;
  state.compareMode = false;
  state.compareReturnHospitalId = null;

  populateLocationFilter();
  populateDateFilter();
  syncFilterControls();
  updateSourceSummary(0);
  render();
}

function matchesText(value, query) {
  if (!query) return true;
  return String(value || "").toLowerCase().includes(query.toLowerCase());
}

function matchesAnyToken(value, query) {
  // Splits the query into individual tokens and returns true if the value
  // contains any token OR any token contains the value. This fixes searches
  // like "乳腺外科" matching "乳腺" in department aliases.
  if (!query) return true;
  const lowerValue = String(value || "").toLowerCase();
  const lowerQuery = query.toLowerCase();
  if (lowerValue.includes(lowerQuery)) return true;
  if (lowerQuery.includes(lowerValue)) return true;
  const tokens = lowerQuery.split(/[,，、\s]+/).filter(Boolean);
  return tokens.some((token) => lowerValue.includes(token) || token.includes(lowerValue));
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    showToast("已复制");
  } catch {
    showToast(text);
  }
}

function showToast(message) {
  let toast = document.querySelector(".toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.className = "toast";
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.classList.add("is-visible");
  window.setTimeout(() => toast.classList.remove("is-visible"), 1400);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll("`", "&#096;");
}

// 全局错误兜底：避免渲染异常静默失败
window.addEventListener("error", (event) => {
  if (event.target && event.target.tagName === "IMG") {
    // 图片加载失败是预期的（外部二维码 URL 可能失效）
    return;
  }
  showToast("页面渲染出错，请刷新重试");
});

window.addEventListener("unhandledrejection", () => {
  showToast("数据加载失败，请检查网络后刷新");
});
