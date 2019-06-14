# -*- coding:utf-8 -*-
__author__ = 'weixuefeng@lubangame.com'
__version__ = ''
__doc__ = ''

import datetime


HEP_KEY = "2b400ed8e5674c31a779475afb5ed1bb"
HEP_SECRET = "3562de4eddba4a1485ffedb9d13eafa7"
HEP_ID = "2178792d3eb04bf6b5dbba19e767e38b"

_REST_API = "rest/v1/"
_HEP_API_BASE_URL = "http://hep.newtonproject.dev.diynova.com/" + _REST_API
# _HEP_API_BASE_URL = "http://127.0.0.1:5000"

HEP_LOGIN = _HEP_API_BASE_URL + "/newnet/caches/auth/"
HEP_PAY = _HEP_API_BASE_URL + "/newnet/caches/pay/"
HEP_PLACE_ORDER = _HEP_API_BASE_URL + "/proofs/"

HEP_PRIVATE_KEY = "0xfd216818cecbc78c0aeb274521b1501a01a2226a23a9a6922abb824b12dd86c4"

HEP_PUBLIC_KEY = '0xb5de35a23f3b21b4c5750d02875af165796e5be673c684e53cf0f022bfe94e5e7df1867816d2869674006e08446bbe6cf21e401545e6e2ee43acc2d20b3ff168 '

SIGN_TYPE = "secp256r1"
QR_CODE_EXPIRED = 300  # second