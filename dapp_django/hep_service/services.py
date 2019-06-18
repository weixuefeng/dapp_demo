# -*- coding:utf-8 -*-
__author__ = 'weixuefeng@lubangame.com'
__version__ = '1.0'
__doc__ = ''
import collections
import hashlib
import json
import time
import uuid

import requests
from fastecdsa import ecdsa
from sha3 import keccak_256

from dapp_django.config import config
from dapp_django.hep_service import constant
import datetime


def hep_login(session_key):
    data = {'uuid': session_key,
            'action': constant.ACTION_LOGIN,
            'scope': 2,
            'expired': int(datetime.datetime.now().timestamp()) + config.QR_CODE_EXPIRED,
            'memo': '1'}
    params = _get_params(data)
    print("params:" + str(params))
    res = requests.post(config.HEP_LOGIN, data=params)
    print(res.content)
    res = json.loads(res.content)
    return res


def hep_pay(params):
    data = {
        'uuid': params['uuid'],
        'action': constant.ACTION_PAY,
        'expired': int(datetime.datetime.now().timestamp()) + config.QR_CODE_EXPIRED,
        'description': params['description'],
        'price_currency': params['price_currency'],
        'total_price': params['total_price'],
        'order_number': params['order_number'],
        'seller': 'NEWID182XXX',
        'customer': params['customer'],
        'broker': 'NEWIDXXX',
    }
    params = _get_params(data)
    res = requests.post(config.HEP_PAY, data=params)
    print(res.content)
    res = json.loads(res.content)
    return res


def hep_proof(params):
    data = {
        'content': params['order'],
        'action': constant.ACTION_PROOF_SUBMIT,
        'uuid': params['uuid'],
    }
    params = _get_params(data)
    print("params:" + str(params))
    res = requests.post(config.HEP_PLACE_ORDER, json=params)
    res = json.loads(res.content)
    print(res)
    return res


def sign_request_params(data):
    base_params = _get_h5_base_params()
    data.update(base_params)
    sign_string = get_sign_string(data, "&")
    data['signature'] = _sign_r1(sign_string, private_key=config.HEP_PRIVATE_KEY)
    return data


def _get_params(data):
    base_params = _get_base_params()
    data.update(base_params)
    sign_string = get_sign_string(data, "&")
    data['dapp_signature'] = generate_digest(sign_string, secret=config.HEP_SECRET)
    signature = _sign_r1(sign_string, private_key=config.HEP_PRIVATE_KEY)
    print("signstring:\r\n" + sign_string)
    data['signature'] = signature
    data['sign_type'] = config.SIGN_TYPE
    return data


def _get_base_params():
    params = {'dapp_id': config.HEP_ID,
              'dapp_key': config.HEP_KEY,
              'protocol': 'HEP',
              'version': '1.0',
              'ts': int(time.time()),
              'nonce': uuid.uuid4().hex,
              'os': 'web',
              'language': 'zh',
              'dapp_signature_method': 'HMAC-MD5'
              }
    return params


def _get_h5_base_params():
    params = {'dapp_id': config.HEP_ID,
              'protocol': 'HEP',
              'version': '1.0',
              'ts': int(time.time()),
              'nonce': uuid.uuid4().hex,
              'sign_type': config.SIGN_TYPE,
              }
    return params


def sign_hmac(data, prefix='', join='&'):
    data = collections.OrderedDict(sorted(data.items()))
    sign_string = prefix
    n = 0
    for k, v in data.items():
        if n != 0 and k != 'sign':
            sign_string += join
        n += 1
        if k != 'sign':
            sign_string += u'%s=%s' % (k, v)
    return sign_string


def generate_digest(data, secret):
    return hashlib.md5((data + secret).encode('utf-8')).hexdigest()


def _sign_r1(message, private_key='', hashfunc=keccak_256):
    r, s = ecdsa.sign(message, int(private_key, 16), hashfunc=hashfunc)
    res = '0x%s%s' % (_adjust_sign_str(str(hex(r))), _adjust_sign_str(str(hex(s))))
    return res


def _adjust_sign_str(sign_str):
    if sign_str.startswith('0x'):
        sign_str = sign_str.replace('0x', '')
    return '0' * (64 - len(sign_str)) + sign_str


def get_sign_string(data, joint):
    ordered_data = collections.OrderedDict(sorted(data.items()))
    sign_string = ''
    sign_fields = ['dapp_signature', 'signature', 'sign_type', 'dapp_signature_method']
    n = 0
    for k, v in ordered_data.items():
        if k in sign_fields:
            continue
        if n != 0:
            sign_string += joint
        n += 1
        if isinstance(v, list) or isinstance(v, dict):
            sign_string += u'%s=%s' % (k, json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=False))
        else:
            sign_string += u'%s=%s' % (k, v)
    return sign_string


if __name__ == "__main__":
    str = ''
    print(generate_digest("1"))


