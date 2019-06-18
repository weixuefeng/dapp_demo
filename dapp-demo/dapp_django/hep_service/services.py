# -*- coding:utf-8 -*-
__author__ = 'weixuefeng@lubangame.com'
__version__ = '1.0'
__doc__ = ''
import datetime
import json
import uuid
import sys
import hep_rest_api
from hep_rest_api import utils
from hep_rest_api import models

import requests
from django.conf import settings
from dapp_django.config import config
from dapp_django.hep_service import constant


def hep_login(session_key):
    data = {'uuid': session_key,
            'action': constant.ACTION_LOGIN,
            'scope': 2,
            'expired': int(datetime.datetime.now().timestamp()) + config.QR_CODE_EXPIRED,
            'memo': '1'}
    data = _sign_data(data)
    api_client = _get_api_client()
    if api_client:
        auth_cache = models.AuthCacheRequest(**data)
        res = api_client.rest_newnet_caches_auth_create(body=auth_cache, api_version="1")
        return res.auth_hash
    return None


def hep_pay(params):
    data = {
        'uuid': params['uuid'],
        'action': constant.ACTION_PAY,
        'expired': int(datetime.datetime.now().timestamp()) + config.QR_CODE_EXPIRED,
        'description': params['description'],
        'price_currency': params['price_currency'],
        'total_price': params['total_price'],
        'order_number': params['order_number'],
        'seller': params['customer'],
        'customer': params['customer'],
        'broker': params['customer'],
    }
    data = _sign_data(data)
    api_client = _get_api_client()
    if api_client:
        pay_cache = models.PayCacheRequest(**data)
        res = api_client.rest_newnet_caches_pay_create(body=pay_cache, api_version="1")
        return res.pay_hash
    return None


def hep_proof(params):
    data = {
        'content': params['order'],
        'action': constant.ACTION_PROOF_SUBMIT,
        'uuid': params['uuid'],
    }
    data = _sign_data(data)
    api_client = _get_api_client()
    if api_client:
        proof_cache = models.CreateProofRequest(**data)
        res = api_client.rest_proofs_create(body=proof_cache, api_version="1")
        return res.proof_hash
    return None


def _get_api_client():
    configuration = hep_rest_api.api_client.Configuration()
    configuration.host = constant.HEP_HOST
    api_instance = hep_rest_api.RestApi(hep_rest_api.ApiClient(configuration))
    return api_instance


def _get_base_data():
    dapp_id = constant.HEP_ID
    dapp_key = constant.HEP_KEY
    dapp_secret = constant.HEP_SECRET
    protocol = constant.HEP_PROTOCOL
    version = constant.HEP_PROTOCOL_VERSION
    ts = int(datetime.datetime.now().timestamp())
    nonce = uuid.uuid4().hex
    os = sys.platform
    language = 'en'
    dapp_signature_method = 'HMAC-MD5'
    dapp_signature = ''

    data = {
        'dapp_id': dapp_id,
        'dapp_key': dapp_key,
        'protocol': protocol,
        'version': version,
        'ts': ts,
        'nonce': nonce,
        'os': os,
        'language': language,
        'dapp_signature_method': dapp_signature_method,
        'sign_type': constant.SIGN_TYPE
    }
    return data


def _sign_data(data):
    try:
        base_data = _get_base_data()
        data.update(base_data)
        dapp_signature = utils.sign_hmac(data, constant.HEP_SECRET)
        data['dapp_signature'] = dapp_signature
        sign_string = utils.generate_signature_base_string(data, "&")
        r, s = utils.sign_secp256r1(sign_string, settings.PRIVATE_KEY_PATH)
        if r.startswith('0x'):
            r = r.replace('0x', '')
        if s.startswith('0x'):
            s = s.replace('0x', '')
        data['signature'] = '0x' + r + s
        return data
    except Exception as e:
        print(e.args)
        return None


if __name__ == "__main__":
    str = ''



