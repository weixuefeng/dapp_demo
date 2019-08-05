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
NEWCHAIN_RPC_URL = 'https://devnet.newchain.cloud.diynova.com'

RELEASE = False
if RELEASE:
    HEP_KEY = "e3e3b730955d4f7ca405645f17c6dd1d"
    HEP_SECRET = "70dc942a981e469686c5b94108393eb9"
    HEP_ID = "ad153ffe8cff4677ae2edd5d5670d408"
    HEP_HOST = "https://node.hep.testnet.newtonproject.org/"
    CHAIN_ID = 1007
else:
    HEP_KEY = "02c3119710714730b000db31d73052ce"
    HEP_SECRET = "eae92dbda0454049b8016a43c2d7025e"
    HEP_HOST = "http://hep.newtonproject.dev.diynova.com"
    HEP_ID = "d32db928a0034598a69bdf375551f822"
    CHAIN_ID = 1002

HEP_PROTOCOL = "HEP"
HEP_PROTOCOL_VERSION = "1.0"
_REST_API = "rest/v1/"
# _HEP_API_BASE_URL = "http://127.0.0.1:5000"

HEP_LOGIN = HEP_HOST + "/newnet/caches/auth/"
HEP_PAY = HEP_HOST + "/newnet/caches/pay/"
HEP_PLACE_ORDER = HEP_HOST + "/proofs/"
HEP_PRIVATE_KEY = "0xfd216818cecbc78c0aeb274521b1501a01a2226a23a9a6922abb824b12dd86c4"

HEP_PUBLIC_KEY = '0x55da361207ad16a68b3cfd5551e08148862a409f3a25f8ecdb2b2ad78074a8bb915aeae0f8ebbf2d1fe68ec47e246b20c6f07b3733836496062bf8f3401bbc4f'

SIGN_TYPE = "secp256r1"
QR_CODE_EXPIRED = 300  # second

ACTION_LOGIN = "hep.auth.login"
ACTION_PAY = "hep.pay.order"
ACTION_PROOF_SUBMIT = "hep.proof.submit"
PRIVATE_KEY_PATH = "/Users/erhu/project/gitrepo/dapp_django/dapp-demo/priv"
#DAPP_ID_ANDROID = "30eafeee9337469bb862397ac25bcd80"
#DAPP_ID_IOS = "a4003fccf6f742c280dc0a2a862e80c1"
#DAPP_ID_ANDROID_PRIVATE_PATH = "/data/www/temp/priv/android"
#DAPP_ID_IOS_PRIVATE_PATH = "/data/www/temp/priv/ios"
#DAPP_KEY_ANDROID = "cc89a141011d4631bc673b6a81a7df90"
#DAPP_SECRET_ANDROID = "29560e882c774455ada20e48c46306e6"
#DAPP_KEY_IOS = "e48e66911604453698e359cc84c498d0"
#DAPP_SECRET_IOS = "9b6ea1d0505d49e4b3b94e07374ef081"
DAPP_ID_ANDROID = HEP_ID
DAPP_ID_IOS = HEP_ID
DAPP_ID_ANDROID_PRIVATE_PATH = PRIVATE_KEY_PATH
DAPP_ID_IOS_PRIVATE_PATH = PRIVATE_KEY_PATH
DAPP_KEY_ANDROID = HEP_KEY
DAPP_SECRET_ANDROID = HEP_SECRET
DAPP_KEY_IOS = HEP_KEY
DAPP_SECRET_IOS = HEP_SECRET
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    }
}
