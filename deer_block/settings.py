import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#kyxtl177*d)kv^+2xi5w!e)m-6bm%jg#(me7_3lrzpnfd=uh3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
APPEND_SLASH = True

# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'apps.users.apps.UserConfig',
    'apps.media.apps.MediaConfig',
    'apps.square.apps.SquareConfig',
    'apps.artwork.apps.ProductConfig',
    'apps.business.apps.BusinessConfig',
    'apps.shop.apps.ShopConfig',
    'minio_storage',
]

# 依照此顺序进行验证
AUTHENTICATION_BACKENDS = (
    'apps.users.backends.CustomBackend',
    'apps.users.backends.MobileTokenModelBackend',
)

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middlewares.logger_middleware.LogMiddle',
]

ROOT_URLCONF = 'deer_block.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'deer_block.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_NAME", 'deer_block'),
        'USER': os.environ.get("POSTGRES_USER", 'postgres'),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD", '123456'),
        'HOST': os.environ.get("POSTGRES_HOST", 'localhost'),
        'PORT': os.environ.get("POSTGRES_PORT", '15432'),

    },
}

# redis配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}/0".format(os.environ.get("CACHE_LOCATION_IP", '127.0.0.1'),
                                             os.environ.get("CACHE_LOCATION_PORT", '16379')),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
        }
    },
}

# redis缓存时间
REDIS_TIMEOUT = 60 * 60 * 24 * 15

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DATE_FORMAT = 'Y-m-d'

DATETIME_FORMAT = 'Y-m-d H:i:s'

# cookies 相关的设置
SESSION_COOKIE_AGE = 60 * 60 * 12
SESSION_SAVE_EVERY_REQUEST = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 用了oss后可能这个配置就无效了，记录在此

# # 阿里云OSS配置
# OSS_ACCESS_KEY_ID = os.environ.get("OSS_ACCESS_KEY_ID")
# OSS_ACCESS_KEY_SECRET = os.environ.get("OSS_ACCESS_KEY_SECRET")
# OSS_ENDPOINT = os.environ.get("OSS_ENDPOINT")  # 访问域名, 根据服务器上的实际配置修改
# OSS_BUCKET_NAME = os.environ.get("OSS_BUCKET_NAME")  # oss 创建的 BUCKET 名称
# DEFAULT_FILE_STORAGE = 'django_oss_storage.backends.OssMediaStorage'

# minio配置
DEFAULT_FILE_STORAGE = "minio_storage.storage.MinioMediaStorage"
MINIO_STORAGE_ENDPOINT = '{}:{}'.format(os.environ.get("MINIO_SET_IP"), os.environ.get("MINIO_SET_PORT"))
MINIO_STORAGE_ACCESS_KEY = os.environ.get("MINIO_STORAGE_ACCESS_KEY")
MINIO_STORAGE_SECRET_KEY = os.environ.get("MINIO_STORAGE_SECRET_KEY")
MINIO_STORAGE_USE_HTTPS = False
MINIO_STORAGE_MEDIA_BUCKET_NAME = 'media'
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'apps.paginations.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    'UNICODE_JSON': True,
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_THROTTLE_CLASSES': (
        # 反爬虫
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/second',
        'user': '30/second'
    },
    'EXCEPTION_HANDLER': 'exceptions.base_excption.custom_exception_handler',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 文件上传限制最大50M大小

BASE_LOG_DIR = os.path.join(BASE_DIR, "logs")
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                      '[%(levelname)s][%(message)s]'
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
        'collect': {
            'format': '%(message)s'
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，根据文件大小自动切
            'filename': os.path.join(BASE_LOG_DIR, "fs_info.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 10,  # 备份数为3  xx.log --> xx.log.1 --> xx.log.2 --> xx.log.3
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "fs_err.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'django': {  # 默认的logger应用如下配置
            'handlers': ['info', 'console', 'error'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['info', 'console'],
            'level': 'INFO',
            'propagate': False  # 是否向上一级logger实例传递日志信息
        },
        'django.test': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
    },
}

SEND_MSG_MODE = os.environ.get("SEND_MSG_MODE")

# 阿里云发送短信服务的子账号密码
SEND_MESSAGE_ACCESS_KEY = os.environ.get("SEND_MESSAGE_ACCESS_KEY")
SEND_MESSAGE_ACCESS_SECRET = os.environ.get("SEND_MESSAGE_ACCESS_SECRET")

# 配置阿里云发送短信的模版、签名等，根据不同的功能配置不同的模版和签名
ALI_SEND_CONFIG = {
    # register and login
    "ral": {
        "sign_name": os.environ.get("SIGN_NAME"),
        "template_code": os.environ.get("TEMPLATE_CODE"),
    },
}

# celery 配置
# Broker配置，使用Redis作为消息中间件
BROKER_URL = "redis://{}:{}/1".format(os.environ.get("CACHE_LOCATION_IP", '127.0.0.1'),
                                      os.environ.get("CACHE_LOCATION_PORT", '16379'))
# BACKEND配置，这里使用redis
CELERY_RESULT_BACKEND = "redis://{}:{}/1".format(os.environ.get("CACHE_LOCATION_IP", '127.0.0.1'),
                                                 os.environ.get("CACHE_LOCATION_PORT", '16379'))
# 结果序列化方案
CELERY_RESULT_SERIALIZER = 'json'
# 任务结果过期时间，秒
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
# 时区配置
CELERY_TIMEZONE = TIME_ZONE

# websocket
WS_URL = "ws://{}:{}/".format(os.environ.get("WS_IP", 'localhost'),
                              os.environ.get("WS_PORT", '18000'))
