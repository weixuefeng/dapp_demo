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


def hep_login(session_key):
    data = {'uuid': session_key,
            'action': constant.ACTION_LOGIN,
            'scope': 2,
            'expired': config.QR_CODE_EXPIRED,
            'memo': 'Demo Request Login',
            'sign_type': config.SIGN_TYPE}
    params = _get_params(data)
    res = requests.post(config.HEP_LOGIN, data=params)
    res = json.loads(res.content)
    return res


def hep_pay(params):
    data = {
        'uuid': params['uuid'],
        'action': constant.ACTION_PAY,
        'expired': config.QR_CODE_EXPIRED,
        'description': params['description'],
        'price_currency': params['price_currency'],
        'total_price': params['total_price'],
        'order_number': params['order_number'],
        'seller': 'NEWID182XXX',
        'customer': params['customer'],
        'broker': 'NEWIDXXX',
        'sign_type': 'spec256r1'
    }
    params = _get_params(data)
    res = requests.post(config.HEP_PAY, data=params)
    print(res)
    res = json.loads(res.content)
    return res


def hep_proof(params):
    data = {
        'content': params['order'],
        'action': constant.ACTION_PROOF_SUBMIT,
        'uuid': params['uuid'],
        'sign_type': config.SIGN_TYPE
    }
    params = _get_params(data)
    res = requests.post(config.HEP_PLACE_ORDER, data=params)
    res = json.loads(res.content)
    return res


def _get_params(data):
    base_params = _get_base_params()
    data.update(base_params)
    sign_string = sign_hmac(data, secret=config.HEP_SECRET)
    data['md5'] = generate_digest(sign_string)
    signature = _sign_r1(sign_string, private_key=config.HEP_PRIVATE_KEY)
    data['signature'] = signature
    return data


def _get_base_params():
    params = {'dapp_id': config.HEP_ID,
              'dapp_key': config.HEP_KEY,
              'protocol': 'HEP',
              'version': '1.0',
              'ts': int(time.time()),
              'nonce': uuid.uuid4().hex}
    return params


def sign_hmac(data, secret, prefix='', join='&'):
    data = collections.OrderedDict(sorted(data.items()))
    sign_string = prefix
    n = 0
    for k, v in data.items():
        if n != 0 and k != 'sign':
            sign_string += join
        n += 1
        if k != 'sign':
            sign_string += u'%s=%s' % (k, v)
    sign_string += secret
    return sign_string


def generate_digest(data):
    return hashlib.md5(data.encode('utf-8')).hexdigest()


def _sign_r1(message, private_key='', hashfunc=keccak_256):
    r, s = ecdsa.sign(message, int(private_key, 16), hashfunc=hashfunc)
    res = '0x%s%s' % (_adjust_sign_str(str(hex(r))), _adjust_sign_str(str(hex(s))))
    return res


def _adjust_sign_str(sign_str):
    if sign_str.startswith('0x'):
        sign_str = sign_str.replace('0x', '')
    return '0' * (64 - len(sign_str)) + sign_str


if __name__ == "__main__":
    hep_login('session_key')


