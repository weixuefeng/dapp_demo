# -*- coding:utf-8 -*-
__author__ = 'weixuefeng@lubangame.com'
__version__ = ''
__doc__ = ''


HEP_KEY = "2eb603961aba4bf28cee101384b18b68"
HEP_SECRET = "60a0a51c47ae4c8c8656e4046b5bb394"
HEP_ID = "41a9bd28e1324bd28566cbafa9a4e064"
HEP_PROTOCOL = "HEP"
HEP_PROTOCOL_VERSION = "1.0"
_REST_API = "rest/v1/"
HEP_HOST = "http://hep.newtonproject.dev.diynova.com/" + _REST_API
# _HEP_API_BASE_URL = "http://127.0.0.1:5000"

HEP_LOGIN = HEP_HOST + "/newnet/caches/auth/"
HEP_PAY = HEP_HOST + "/newnet/caches/pay/"
HEP_PLACE_ORDER = HEP_HOST + "/proofs/"

HEP_PRIVATE_KEY = "0xfd216818cecbc78c0aeb274521b1501a01a2226a23a9a6922abb824b12dd86c4"

HEP_PUBLIC_KEY = '0xb5de35a23f3b21b4c5750d02875af165796e5be673c684e53cf0f022bfe94e5e7df1867816d2869674006e08446bbe6cf21e401545e6e2ee43acc2d20b3ff168 '

SIGN_TYPE = "secp256r1"
QR_CODE_EXPIRED = 300  # second

ACTION_LOGIN = "hep.auth.login"
ACTION_PAY = "hep.pay.order"
ACTION_PROOF_SUBMIT = "hep.proof.submit"
