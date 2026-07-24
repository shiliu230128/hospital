window.PROTOTYPE_LATEST_REPORT = {
  "generatedAt": "2026-07-24T16:38:52+08:00",
  "mode": "manual_one_shot_runner",
  "automationStatus": {
    "currentlyAutomatic": false,
    "selectedRuntime": "project_script_only",
    "dailyAutomationReady": true,
    "howToAutomateLater": [
      "launchd/cron/Comate Automation can call: python3 data-access-research/update_data_once.py",
      "Treat non-zero exit or report.overallStatus != pass as an alert.",
      "Do not auto-promote discovery candidates into frontend data without manual official-source verification."
    ]
  },
  "wechatCandidateRefresh": {
    "skipped": true,
    "reason": "quick refresh skips WeChat candidate crawling"
  },
  "wechatAssetCleanup": {
    "assetDirExists": true,
    "keptCount": 32,
    "deletedCount": 0,
    "deletedBytes": 0,
    "keptFiles": [
      "assets/wechat-qrcodes/bj_chaoyang-22.jpg",
      "assets/wechat-qrcodes/bjogh-13.png",
      "assets/wechat-qrcodes/bjxk-3.jpg",
      "assets/wechat-qrcodes/hz_childrens-3.jpg",
      "assets/wechat-qrcodes/hz_first-7.png",
      "assets/wechat-qrcodes/hz_normal_affiliated-0.png",
      "assets/wechat-qrcodes/hz_normal_affiliated-1.png",
      "assets/wechat-qrcodes/hz_normal_affiliated-2.png",
      "assets/wechat-qrcodes/hz_seventh-1.png",
      "assets/wechat-qrcodes/hz_women-1.jpg",
      "assets/wechat-qrcodes/hz_zcmu2-1.jpg",
      "assets/wechat-qrcodes/pumch-0.jpg",
      "assets/wechat-qrcodes/sh_changhai-0.jpg",
      "assets/wechat-qrcodes/sh_first_maternity-10.png",
      "assets/wechat-qrcodes/sh_huashan-3.jpg",
      "assets/wechat-qrcodes/sh_huashan-6.jpg",
      "assets/wechat-qrcodes/sh_longhua-1.jpg",
      "assets/wechat-qrcodes/sh_longhua-2.jpg",
      "assets/wechat-qrcodes/sh_longhua-3.jpg",
      "assets/wechat-qrcodes/sh_mental-13.png",
      "assets/wechat-qrcodes/sh_public_health-0.jpg",
      "assets/wechat-qrcodes/sh_pulmonary-3.jpg",
      "assets/wechat-qrcodes/sh_shuguang-1.jpg",
      "assets/wechat-qrcodes/sh_shuguang-2.jpg",
      "assets/wechat-qrcodes/sh_tumor_fudan-22.jpg",
      "assets/wechat-qrcodes/sh_tumor_fudan-25.jpg",
      "assets/wechat-qrcodes/sh_yueyang-3.jpg",
      "assets/wechat-qrcodes/sz_luohu_people-2.png",
      "assets/wechat-qrcodes/sz_luohu_people-4.png",
      "assets/wechat-qrcodes/sz_people-0.jpg",
      "assets/wechat-qrcodes/sz_tcm-6.jpg",
      "assets/wechat-qrcodes/xuanwu-5.jpg"
    ],
    "deletedFilesSample": [],
    "policy": "Keep only local QR images referenced by frontend-prototype/wechat-entries.js; downloaded candidates are transient."
  },
  "wechatEntryValidation": {
    "hospitalCount": 47,
    "entryCount": 63,
    "payloadCount": 62,
    "badPayloads": [],
    "missingLocalAssets": [],
    "status": "pass"
  },
  "registryAudit": {
    "city": "北京",
    "localRegistryCount": 57,
    "officialSeedCount": 43,
    "missingFromLocalRegistry": [],
    "likelyDuplicates": [],
    "mediumConfidenceItems": [
      {
        "id": "cpzxy",
        "name": "北京市昌平区中西医结合医院",
        "reason": "registryConfidence is not high"
      },
      {
        "id": "yuquan",
        "name": "清华大学玉泉医院",
        "reason": "registryConfidence is not high"
      },
      {
        "id": "beijing_geriatric",
        "name": "北京老年医院",
        "reason": "registryConfidence is not high"
      },
      {
        "id": "luhe",
        "name": "首都医科大学附属北京潞河医院",
        "reason": "registryConfidence is not high"
      },
      {
        "id": "pla_general",
        "name": "中国人民解放军总医院",
        "reason": "registryConfidence is not high"
      },
      {
        "id": "pla_305",
        "name": "中国人民解放军第三〇五医院",
        "reason": "registryConfidence is not high"
      },
      {
        "id": "pla_airforce",
        "name": "中国人民解放军空军特色医学中心",
        "reason": "registryConfidence is not high"
      },
      {
        "id": "pla_rocket",
        "name": "中国人民解放军火箭军特色医学中心",
        "reason": "registryConfidence is not high"
      },
      {
        "id": "pla_general_ninth",
        "name": "中国人民解放军总医院第九医学中心",
        "reason": "registryConfidence is not high"
      },
      {
        "id": "pla_general_second",
        "name": "中国人民解放军总医院第二医学中心",
        "reason": "registryConfidence is not high"
      },
      {
        "id": "pla_general_third",
        "name": "中国人民解放军总医院第三医学中心",
        "reason": "registryConfidence is not high"
      },
      {
        "id": "pla_general_fourth",
        "name": "中国人民解放军总医院第四医学中心",
        "reason": "registryConfidence is not high"
      },
      {
        "id": "pla_general_fifth_south",
        "name": "中国人民解放军总医院第五医学中心南院区",
        "reason": "registryConfidence is not high"
      },
      {
        "id": "pla_airforce_north",
        "name": "中国人民解放军空军特色医学中心北院区",
        "reason": "registryConfidence is not high"
      },
      {
        "id": "pkuih",
        "name": "北京大学国际医院",
        "reason": "registryConfidence is not high"
      }
    ],
    "policy": "Seed list is used for gap detection only. New hospitals require official-source verification before frontend promotion."
  },
  "multiCityRegistryAudit": {
    "cityCount": 4,
    "totalHospitalCount": 131,
    "totalSourceEntryCount": 131,
    "citiesWithMissingEntries": [],
    "citiesWithTargetSeedGaps": [],
    "byCity": {
      "北京": {
        "hospitalCount": 57,
        "sourceEntryCount": 57,
        "sourceStatusCounts": {
          "official": 51,
          "manual_unverified": 5,
          "official_public": 1
        },
        "missingSourceEntries": [],
        "targetSeedCount": 43,
        "missingFromTargetSeed": [],
        "mediumConfidenceItems": [
          {
            "id": "cpzxy",
            "name": "北京市昌平区中西医结合医院",
            "confidence": "medium"
          },
          {
            "id": "yuquan",
            "name": "清华大学玉泉医院",
            "confidence": "medium"
          },
          {
            "id": "beijing_geriatric",
            "name": "北京老年医院",
            "confidence": "medium"
          },
          {
            "id": "luhe",
            "name": "首都医科大学附属北京潞河医院",
            "confidence": "medium"
          },
          {
            "id": "pla_general",
            "name": "中国人民解放军总医院",
            "confidence": "medium"
          },
          {
            "id": "pla_305",
            "name": "中国人民解放军第三〇五医院",
            "confidence": "medium"
          },
          {
            "id": "pla_airforce",
            "name": "中国人民解放军空军特色医学中心",
            "confidence": "medium"
          },
          {
            "id": "pla_rocket",
            "name": "中国人民解放军火箭军特色医学中心",
            "confidence": "medium"
          },
          {
            "id": "pla_general_ninth",
            "name": "中国人民解放军总医院第九医学中心",
            "confidence": "medium"
          },
          {
            "id": "pla_general_second",
            "name": "中国人民解放军总医院第二医学中心",
            "confidence": "medium"
          },
          {
            "id": "pla_general_third",
            "name": "中国人民解放军总医院第三医学中心",
            "confidence": "medium"
          },
          {
            "id": "pla_general_fourth",
            "name": "中国人民解放军总医院第四医学中心",
            "confidence": "medium"
          },
          {
            "id": "pla_general_fifth_south",
            "name": "中国人民解放军总医院第五医学中心南院区",
            "confidence": "medium"
          },
          {
            "id": "pla_airforce_north",
            "name": "中国人民解放军空军特色医学中心北院区",
            "confidence": "medium"
          },
          {
            "id": "pkuih",
            "name": "北京大学国际医院",
            "confidence": "medium"
          }
        ],
        "likelyDuplicates": []
      },
      "上海": {
        "hospitalCount": 33,
        "sourceEntryCount": 33,
        "sourceStatusCounts": {
          "official": 33
        },
        "missingSourceEntries": [],
        "targetSeedCount": 33,
        "missingFromTargetSeed": [],
        "mediumConfidenceItems": [],
        "likelyDuplicates": []
      },
      "深圳": {
        "hospitalCount": 23,
        "sourceEntryCount": 23,
        "sourceStatusCounts": {
          "official": 15,
          "official_public": 8
        },
        "missingSourceEntries": [],
        "targetSeedCount": 23,
        "missingFromTargetSeed": [],
        "mediumConfidenceItems": [],
        "likelyDuplicates": []
      },
      "杭州": {
        "hospitalCount": 18,
        "sourceEntryCount": 18,
        "sourceStatusCounts": {
          "official": 15,
          "official_public": 3
        },
        "missingSourceEntries": [],
        "targetSeedCount": 18,
        "missingFromTargetSeed": [],
        "mediumConfidenceItems": [],
        "likelyDuplicates": []
      }
    },
    "policy": "This audit checks both source-entry completeness and target seed-list coverage. It does not promote scraped candidates or claim realtime availability.",
    "status": "pass"
  },
  "sourceHealth": [
    {
      "id": "beijing_wjw_home",
      "name": "北京市卫生健康委员会官网",
      "url": "https://wjw.beijing.gov.cn",
      "ok": true,
      "status": 200,
      "elapsedMs": 611,
      "bytes": 161599,
      "contentType": "text/html; charset=utf-8",
      "expectedTextFound": true,
      "level": "official_directory_signal",
      "capability": "source_reachability"
    },
    {
      "id": "nhc_service_query",
      "name": "国家卫健委政务服务平台查询入口",
      "url": "https://zwfw.nhc.gov.cn/cxx",
      "ok": true,
      "status": 200,
      "elapsedMs": 1426,
      "bytes": 13084,
      "contentType": "text/html",
      "expectedTextFound": true,
      "level": "official_query_entry",
      "capability": "source_reachability"
    },
    {
      "id": "bj_114_entry",
      "name": "北京市预约挂号统一平台入口探测",
      "url": "https://www.114yygh.com/robots.txt",
      "ok": true,
      "status": 200,
      "elapsedMs": 331,
      "bytes": 2840,
      "contentType": "text/html",
      "expectedTextFound": true,
      "level": "official_registration_entry_only",
      "capability": "source_reachability"
    }
  ],
  "scheduleSamples": {
    "samples": [
      {
        "hospitalId": "bch",
        "level": "L1",
        "status": "sample_available",
        "recordCount": 1168,
        "sourceNote": ""
      },
      {
        "hospitalId": "puh3",
        "level": "L1",
        "status": "sample_available",
        "recordCount": 93,
        "sourceNote": "北京大学第三医院官网公开出停诊信息接口样本。该样本为公开排班/停诊/门诊限号信息，不代表授权实时余号。"
      },
      {
        "hospitalId": "pumch",
        "level": "L1",
        "status": "sample_available",
        "recordCount": 122,
        "sourceNote": "北京协和医院官网公开门诊出诊表。该数据为公开排班，不代表实时余号。"
      }
    ],
    "sampleCount": 3
  },
  "liveAvailabilityProbe": {
    "policy": "Low-frequency public endpoint checks only; no login, CAPTCHA, WAF bypass, order flow, or personal-data collection.",
    "probes": [
      {
        "id": "bch_public_schedule",
        "name": "bch_public_schedule",
        "url": "http://www.bch.com.cn/Html/Hospitals/Schedulings/OPIndex0_0.html",
        "ok": true,
        "status": 200,
        "elapsedMs": 370,
        "bytes": 1225402,
        "contentType": "text/html",
        "expectedTextFound": true,
        "level": "L1",
        "capability": "public_schedule_html"
      },
      {
        "id": "puh3_campus_api",
        "name": "puh3_campus_api",
        "url": "https://www.puh3.net.cn/aop_web/industry/patient/static/userHospital/allEnable",
        "ok": true,
        "status": 200,
        "elapsedMs": 200,
        "bytes": 1941,
        "contentType": "application/json",
        "expectedTextFound": true,
        "level": "L1",
        "capability": "public_schedule_api_seed"
      },
      {
        "id": "pumch_public_schedule",
        "name": "pumch_public_schedule",
        "url": "https://www.pumch.cn/dsearchs/dockervisit/3/1.html",
        "ok": true,
        "status": 200,
        "elapsedMs": 3667,
        "bytes": 1367350,
        "contentType": "text/html",
        "expectedTextFound": true,
        "level": "L1",
        "capability": "public_schedule_html"
      },
      {
        "id": "yygh_hospital_list",
        "name": "yygh_hospital_list",
        "url": "https://www.114yygh.com/web/hospital/list",
        "ok": true,
        "status": 202,
        "elapsedMs": 178,
        "bytes": 1855,
        "contentType": "text/html; charset=utf-8",
        "expectedTextFound": false,
        "level": "unknown",
        "capability": "unauthorized_public_list_probe"
      }
    ],
    "successRates": {
      "publicScheduleL1": "3/3",
      "realtimeL3L4Positive": "0/0 configured"
    }
  },
  "priorAvailabilitySummary": {
    "status": "loaded",
    "generatedAt": "2026-06-30T23:10:00+08:00",
    "sourceCount": 5,
    "levelCounts": {
      "L1": 3,
      "L2-structure-found-L3L4-not-proven": 1,
      "L0-entry-only": 1
    },
    "positiveRealtimeSources": [],
    "overallConclusion": "BCH, PUH3 and PUMCH public pages can support real public schedule comparison. PUMCH H5 exposes promising availability-shaped fields, but the probe did not prove a positive doctor-date-time-slot bookable case. A user-facing 'only available slots' feature should wait until L3/L4 data is legally and stably available."
  },
  "generatedArtifactRetention": {
    "directoryExists": false,
    "deletedCount": 0,
    "keptCount": 0
  },
  "overallStatus": "pass"
};
