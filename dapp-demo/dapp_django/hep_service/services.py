# -*- coding:utf-8 -*-
__author__ = 'weixuefeng@lubangame.com'
__version__ = '1.0'
__doc__ = ''
import datetime
import sys
import uuid

from django.conf import settings
import hep_rest_api

from hep_rest_api.scenarios.auth import AuthHelper
from hep_rest_api.scenarios.pay import PayHelper
from hep_rest_api.scenarios.proof import ProofHelper
from hep_rest_api.scenarios.proof import OrderProof


api_client = None

base_parameters = {
    'dapp_key': settings.HEP_KEY,
    'protocol': settings.HEP_PROTOCOL,
    'version': settings.HEP_PROTOCOL_VERSION,
    'os': sys.platform,
    'language': 'en'
}
chain_id = 1002

auth_helper = None
pay_helper = None
proof_helper = None


def _get_api_client():
    if api_client:
        return api_client
    configuration = hep_rest_api.api_client.Configuration()
    configuration.host = settings.HEP_HOST
    api_instance = hep_rest_api.RestApi(hep_rest_api.ApiClient(configuration))
    return api_instance


def _get_auth_helper():
    if auth_helper:
        return auth_helper
    return AuthHelper(_get_api_client(), base_parameters, settings.HEP_ID, settings.HEP_SECRET, settings.PRIVATE_KEY_PATH, chain_id=chain_id)


def _get_pay_helper():
    if pay_helper:
        return pay_helper
    return PayHelper(_get_api_client(), base_parameters, settings.HEP_ID, settings.HEP_SECRET, settings.PRIVATE_KEY_PATH, chain_id=chain_id)


def _get_proof_helper():
    if proof_helper:
        return proof_helper
    return ProofHelper(_get_api_client(), base_parameters, settings.HEP_ID, settings.HEP_SECRET, settings.PRIVATE_KEY_PATH, chain_id=chain_id)


def hep_login(session_key):
    auth_response = _get_auth_helper().generate_auth_request(uuid=session_key)
    qr_code_str = _get_auth_helper().generate_qrcode_string(auth_response.auth_hash)
    print(qr_code_str)
    return qr_code_str


def verify_profile(data):
    print(data)
    return _get_auth_helper().validate_auth_callback(data)


def hep_pay(params):
    data = {
        'uuid': params['uuid'],
        'action': settings.ACTION_PAY,
        'expired': int(datetime.datetime.now().timestamp()) + settings.QR_CODE_EXPIRED,
        'description': params['description'],
        'price_currency': params['price_currency'],
        'total_price': params['total_price'],
        'order_number': params['order_number'],
        'seller': params['customer'],
        'customer': params['customer'],
        'broker': params['customer'],
    }
    pay_response = _get_pay_helper().generate_pay_request(data['order_number'], data['price_currency'], data['total_price'],
                                                          data['description'], data['seller'],
                                                          data['customer'], data['broker'], uuid=data['uuid'])
    pay_qr_str = _get_pay_helper().generate_qrcode_string(pay_response.pay_hash)
    return pay_qr_str


def verify_pay(params):
    is_valid = _get_pay_helper().validate_pay_callback(params)
    if is_valid:
        response = _get_pay_helper().get_confirmed_transaction(params.get('txid'))
        print(response)
        return response
    return None


def hep_proof(content, uuid):
    proof_response = _get_proof_helper().generate_proof_request(content, uuid=uuid)
    proof_qr_str = _get_proof_helper().generate_qrcode_string(proof_response.proof_hash)
    return proof_qr_str


def verify_proof(data):
    is_valid = _get_proof_helper().validate_proof_callback(data)
    if is_valid:
        proof_hashes = [data.get('proof_hash')]
        response = _get_proof_helper().get_status_of_proofs(proof_hashes)
        return response.receipts[0]
    return None


if __name__ == "__main__":
    str = ''



