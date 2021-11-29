# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

# 开发框架加载顺序：environ.py -> default_settings -> env.py -> default.py -> settings_open_saas.py -> prod.py
import json
from blueapps.conf.default_settings import *  # noqa


RUN_VER = os.getenv("RUN_VER", "open")

OPEN_VER = os.getenv("OPEN_VER", "community")

BK_PAAS_HOST = os.getenv("BK_PAAS_HOST", BK_URL)

BK_PAAS_INNER_HOST = os.getenv("BK_PAAS_INNER_HOST", BK_PAAS_HOST)

BK_PAAS_DESKTOP_HOST = os.getenv(
    "BKAPP_SOPS_PAAS_DESKTOP_HOST",
    "%sconsole/" % BK_PAAS_HOST if BK_PAAS_HOST.endswith("/") else "%s/console/" % BK_PAAS_HOST,
)

BK_CC_HOST = os.getenv("BK_CC_HOST")

BK_JOB_HOST = os.getenv("BK_JOB_HOST")

BK_NODEMAN_HOST = os.getenv("BK_NODEMAN_HOST", "{}/o/bk_nodeman".format(BK_PAAS_HOST))

# paas v2 open
if RUN_VER == "open":
    # SITE_URL,STATIC_URL,,FORCE_SCRIPT_NAME
    # 测试环境
    if os.getenv("BK_ENV") == "testing":
        BK_URL = os.environ.get("BK_URL", "%s/console/" % BK_PAAS_HOST)
        SITE_URL = os.environ.get("BK_SITE_URL", "/t/%s/" % APP_CODE)
        STATIC_URL = "%sstatic/" % SITE_URL
    # 正式环境
    if os.getenv("BK_ENV") == "production":
        BK_URL = os.environ.get("BK_URL", "%s/console/" % BK_PAAS_HOST)
        SITE_URL = os.environ.get("BK_SITE_URL", "/o/%s/" % APP_CODE)
        STATIC_URL = "%sstatic/" % SITE_URL

BK_MONITOR_API_ENTRY = os.getenv("BK_MONITOR_API_ENTRY")
BK_ITSM_API_ENTRY = os.getenv("BK_ITSM_API_ENTRY")
BK_NODEMAN_API_ENTRY = os.getenv("BK_NODEMAN_API_ENTRY")
BK_GSE_KIT_API_ENTRY = os.getenv("BK_GSE_KIT_API_ENTRY")

BKAPP_SOPS_PAAS_ESB_HOST = os.getenv("BKAPP_SOPS_PAAS_ESB_HOST", BK_PAAS_INNER_HOST)

# IAM 相关配置
BKAPP_SOPS_IAM_APP_CODE = os.getenv("BKAPP_SOPS_IAM_APP_CODE", APP_CODE)
BKAPP_SOPS_IAM_APP_SECRET_KEY = os.getenv("BKAPP_SOPS_IAM_APP_SECRET_KEY", SECRET_KEY)
BKAPP_BK_IAM_SYSTEM_ID = os.getenv("BKAPP_BK_IAM_SYSTEM_ID", APP_CODE)
BKAPP_BK_IAM_SYSTEM_NAME = os.getenv("BKAPP_BK_IAM_SYSTEM_NAME", "标准运维")
BK_IAM_V3_APP_CODE = os.getenv("BK_IAM_V3_APP_CODE", "bk_iam")
BK_IAM_SKIP = os.getenv("BK_IAM_SKIP") or os.getenv("BKAPP_IAM_SKIP")
# 兼容 open_paas 版本低于 2.10.7，此时只能从环境变量 BK_IAM_HOST 中获取权限中心后台 host
BK_IAM_INNER_HOST = os.getenv("BK_IAM_V3_INNER_HOST", os.getenv("BK_IAM_HOST", ""))
BK_IAM_SAAS_HOST = os.getenv("BK_IAM_V3_SAAS_HOST", "{}/o/{}".format(BK_PAAS_HOST, BK_IAM_V3_APP_CODE))
# 线上环境IAM配置
BK_IAM_RESOURCE_API_HOST = os.getenv("BKAPP_IAM_RESOURCE_API_HOST", "{}{}".format(BK_PAAS_INNER_HOST, SITE_URL))
# 权限中心 SDK 无权限时不返回 499 的请求路径前缀配置
BK_IAM_API_PREFIX = os.getenv("BKAPP_BK_IAM_API_PREFIX", SITE_URL + "apigw")

# 跨域相关配置
BKAPP_CORS_ALLOW = os.getenv("BKAPP_CORS_ALLOW", None)
BKAPP_CORS_WHITELIST = os.getenv("BKAPP_CORS_WHITELIST", "")

BK_PUSH_URL = os.getenv("BK_PUSH_URL", "")

BK_CELERYD_CONCURRENCY = os.getenv("BK_CELERYD_CONCURRENCY", 2)

BKAPP_PYINSTRUMENT_ENABLE = os.getenv("BKAPP_PYINSTRUMENT_ENABLE", None)

SOPS_MAKO_IMPORT_MODULES = os.getenv("BKAPP_SOPS_MAKO_IMPORT_MODULES", "")

MIGRATE_TOKEN = os.getenv("BKAPP_MIGRATE_TOKEN", "24302cf6-e6a1-11ea-a158-acde48001122")
MIGRATE_ALLOW = os.getenv("BKAPP_MIGRATE_ALLOW", False)

BKAPP_LOG_SHIELDING_KEYWORDS = os.getenv("BKAPP_LOG_SHIELDING_KEYWORDS", "")

# 人员选择数据来源
BK_MEMBER_SELECTOR_DATA_HOST = os.getenv("BKAPP_MEMBER_SELECTOR_DATA_HOST", BK_PAAS_HOST)

# pipeline settings
BKAPP_PIPELINE_RERUN_MAX_TIMES = os.getenv("BKAPP_PIPELINE_RERUN_MAX_TIMES", 50)
BKAPP_PIPELINE_DATA_BACKEND = os.getenv(
    "BKAPP_PIPELINE_DATA_BACKEND", "pipeline.engine.core.data.redis_backend.RedisDataBackend"
)
BKAPP_PIPELINE_DATA_CANDIDATE_BACKEND = os.getenv(
    "BKAPP_PIPELINE_DATA_CANDIDATE_BACKEND", "pipeline.engine.core.data.mysql_backend.MySQLDataBackend"
)

# 是否只允许加载远程 https 仓库的插件
BKAPP_EXTERNAL_PLUGINS_SOURCE_SECURE_LOOSE = os.getenv("BKAPP_EXTERNAL_PLUGINS_SOURCE_SECURE_LOOSE", "1")

# REIDS相关配置
BKAPP_REDIS_HOST = os.getenv("BKAPP_REDIS_HOST")
BKAPP_REDIS_PORT = os.getenv("BKAPP_REDIS_PORT")
BKAPP_REDIS_PASSWORD = os.getenv("BKAPP_REDIS_PASSWORD")
BKAPP_REDIS_SERVICE_NAME = os.getenv("BKAPP_REDIS_SERVICE_NAME")
BKAPP_REDIS_MODE = os.getenv("BKAPP_REDIS_MODE")
BKAPP_REDIS_DB = os.getenv("BKAPP_REDIS_DB")
BKAPP_REDIS_SENTINEL_PASSWORD = os.getenv("BKAPP_REDIS_SENTINEL_PASSWORD")

# CALLBACK 回调地址
BKAPP_INNER_CALLBACK_HOST = os.getenv("BKAPP_INNER_CALLBACK_HOST", BK_PAAS_INNER_HOST + SITE_URL)

BKAPP_FILE_UPLOAD_ENTRY = os.getenv("BKAPP_FILE_UPLOAD_ENTRY", "")

# WEIXIN 配置
BKAPP_WEIXIN_APP_ID = os.getenv("BKAPP_WEIXIN_APP_ID", "")
BKAPP_WEIXIN_APP_SECRET = os.getenv("BKAPP_WEIXIN_APP_SECRET", "")
BKAPP_WEIXIN_APP_EXTERNAL_HOST = os.getenv("BKAPP_WEIXIN_APP_EXTERNAL_HOST", "")

# RSA KEYS, 保存的是密钥的base64加密形式, 使用base64.b64encode(KEY.encode("utf-8"))进行处理后保存为环境变量
RSA_PRIV_KEY = os.getenv("BKAPP_RSA_PRIV_KEY", None)
RSA_PUB_KEY = os.getenv("BKAPP_RSA_PUB_KEY", None)

# 单业务下最大周期任务数量
PERIODIC_TASK_PROJECT_MAX_NUMBER = int(os.getenv("BKAPP_PERIODIC_TASK_PROJECT_MAX_NUMBER", 50))

# 变量名关键字黑名单
VARIABLE_KEY_BLACKLIST = os.getenv("BKAPP_VARIABLE_KEY_BLACKLIST", "context,")

# 任务操作限流开关配置
TASK_OPERATION_THROTTLE = os.getenv("BKAPP_TASK_OPERATION_THROTTLE", False)

# 引擎相关配置
EXPIRED_TASK_CLEAN = False if os.getenv("BKAPP_EXPIRED_TASK_CLEAN") is None else True
EXPIRED_TASK_CLEAN_NUM_LIMIT = int(os.getenv("BKAPP_EXPIRED_TASK_CLEAN_NUM_LIMIT", 100))
TASK_EXPIRED_MONTH = int(os.getenv("BKAPP_TASK_EXPIRED_MONTH", 6))

# 文件管理类型
BKAPP_FILE_MANAGER_TYPE = os.getenv("BKAPP_FILE_MANAGER_TYPE", "")

# JOB 日志提取额外模式配置
try:
    JOB_LOG_VAR_SEARCH_CUSTOM_PATTERNS = json.loads(os.getenv("BKAPP_JOB_LOG_VAR_SEARCH_CUSTOM_PATTERNS", "[]"))
    if not isinstance(JOB_LOG_VAR_SEARCH_CUSTOM_PATTERNS, list):
        JOB_LOG_VAR_SEARCH_CUSTOM_PATTERNS = []
except Exception:
    JOB_LOG_VAR_SEARCH_CUSTOM_PATTERNS = []


# celery broker 连接池数量配置
CELERY_BROKER_POOL_LIMIT = int(os.getenv("BKAPP_CELERY_BROKER_POOL_LIMIT", 10))

# 蓝鲸监控自定义上报配置
BK_MONITOR_REPORT_ENABLE = int(os.getenv("MONITOR_REPORT_ENABLE", 0)) == 1
BK_MONITOR_REPORT_URL = os.getenv("MONITOR_REPORT_URL")
BK_MONITOR_REPORT_DATA_ID = int(os.getenv("MONITOR_REPORT_DATA_ID", -1))
BK_MONITOR_REPORT_ACCESS_TOKEN = os.getenv("MONITOR_REPORT_ACCESS_TOKEN")
BK_MONITOR_REPORT_TARGET = os.getenv("MONITOR_REPORT_TARGET")

# 系统访问地址
BKPAAS_SERVICE_ADDRESSES_BKSAAS = os.getenv("BKPAAS_SERVICE_ADDRESSES_BKSAAS", "")

ENABLE_OTEL_TRACE = os.getenv("BKAPP_ENABLE_OTEL_TRACE", False)

BK_APP_OTEL_INSTRUMENT_DB_API = os.getenv("BKAPP_OTEL_INSTRUMENT_DB_API", False)

NODE_CALLBACK_RETRY_TIMES = int(os.getenv("NODE_CALLBACK_RETRY_TIMES", 3))
