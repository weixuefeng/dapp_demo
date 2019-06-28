import logging
import os
import platform
from logging.handlers import SysLogHandler

# logging
system_string = platform.system()
if system_string == 'Linux':
    syslog_path = '/dev/log'
elif system_string == 'Darwin':
    syslog_path = '/var/run/syslog'
else:
    raise Exception('nonsupport platform!')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING_LEVEL = 'INFO'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s][%(msecs)03d] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'syslog': {
            'level': LOGGING_LEVEL,
            'class': 'logging.handlers.SysLogHandler',
            'facility': SysLogHandler.LOG_LOCAL2,
            'formatter': 'verbose',
            'address': syslog_path,
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', ],
            'level': LOGGING_LEVEL,
        },
        'django': {
            'handlers': ['console', ],
            'propagate': True,
            'level': LOGGING_LEVEL,
        },
        'celery.task': {
            'handlers': ['console', ],
            'propagate': True,
            'level': LOGGING_LEVEL,
        }
    }
}

HEP_PROTOCOL = "HEP"
HEP_PROTOCOL_VERSION = "1.0"
_REST_API = "rest/v1/"
HEP_HOST = "http://hep.newtonproject.dev.diynova.com"
# _HEP_API_BASE_URL = "http://127.0.0.1:5000"

HEP_LOGIN = HEP_HOST + "/newnet/caches/auth/"
HEP_PAY = HEP_HOST + "/newnet/caches/pay/"
HEP_PLACE_ORDER = HEP_HOST + "/proofs/"

HEP_PUBLIC_KEY = '0x7b474af73e15932dbd14cf3f8fd3ad84ecea0afad13c6a4853536b6f41b2e0c4b769cc26632f2a3ee9651ceb184fd64d7e4ddc82056e5f590f88118df48da2c9 '

SIGN_TYPE = "secp256r1"
QR_CODE_EXPIRED = 300  # second

ACTION_LOGIN = "hep.auth.login"
ACTION_PAY = "hep.pay.order"
ACTION_PROOF_SUBMIT = "hep.proof.submit"
CHAIN_ID = 1002
HEP_ID = "75098291f88343b9836118546f375a9f"
HEP_KEY = "71ffeae1a9a2402c944d84c54f8ffddc"
HEP_SECRET = "2d66e7f3dd4445dbb6791b56fadcd2dc"
PRIVATE_KEY_PATH = "/Users/erhu/pony/priv"

DAPP_ID_ANDROID = "ceb2035bacc64fa1b4a90ba19e06d905"
DAPP_ID_ANDROID_PRIVATE_PATH = "/Users/erhu/Desktop/wanqi-android-dev"
DAPP_KEY_ANDROID = "e3cdb3e490e94b06a3f86dba029b9cd8"
DAPP_SECRET_ANDROID = "65ba78af4a1344d49133e8cf53d01ac3"

DAPP_ID_IOS = "a4003fccf6f742c280dc0a2a862e80c1"
DAPP_ID_IOS_PRIVATE_PATH = "/Users/erhu/Downloads/priv_ios"
DAPP_KEY_IOS = "e48e66911604453698e359cc84c498d0"
DAPP_SECRET_IOS = "9b6ea1d0505d49e4b3b94e07374ef081"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    }
}
