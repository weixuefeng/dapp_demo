import datetime
import json
import uuid

from dapp_django.config import codes
from dapp_django.hep_service import services
from dapp_django.utils import http
from django.conf import settings
from django.shortcuts import render
from hep_rest_api import utils
from .models import LoginModel, HepProfileModel, PayModel, ProofModel


def index(request):
    return render(request, "demo/index.html")


def request_login(request):
    try:
        login_session_id = uuid.uuid4().hex
        session_id = login_session_id
        login_model = LoginModel()
        login_model.login_id = session_id
        login_model.save()
        auth_hash = services.hep_login(session_id)
        login = {'auth_hash': auth_hash,
                 'dapp_id': settings.HEP_ID,
                 'action': settings.ACTION_LOGIN,
                 'uuid': session_id
                 }
        request.session['uuid'] = session_id
        return render(request, "demo/hep_login.html", {'login': login})
    except Exception as e:
        print("error")
        print(str(e))
        return http.JsonErrorResponse()


def query_profile(request):
    login_model = LoginModel.objects.filter(login_id=request.session.get('uuid')).first()
    if not login_model:
        return http.JsonErrorResponse(error_message="no login model")
    if login_model.status == codes.StatusCode.AVAILABLE.value:
        return http.JsonSuccessResponse()
    else:
        return http.JsonErrorResponse(error_message="error status")


def user_center(request):
    login_id = request.session['uuid']
    user = HepProfileModel.objects.filter(uuid=login_id).first()
    return render(request, "demo/user.html", {'user': user})


def show_order(request):
    order = {
        "ordername": "芒果",
        "ordernumber": uuid.uuid4().hex,
        "price_currency": "NEW",
        "total_price": "100",
        "order_img": "https://newton-dapp-store.oss-cn-beijing.aliyuncs.com/banner1559375214.png"
    }
    return render(request, "demo/orderlist.html", {'order': order})


def request_pay(request):
    order_number = request.POST.get('order_number')
    login_id = request.session['uuid']
    user = HepProfileModel.objects.filter(uuid=login_id).first()
    pay_session_id = uuid.uuid4().hex
    request.session['pay_id'] = pay_session_id
    pay_model = LoginModel()
    pay_model.login_id = pay_session_id
    pay_model.save()
    order = {
        'uuid': pay_session_id,
        'description': '你好',
        'price_currency': 'NEW',
        'total_price': '100',
        'order_number': order_number,
        'seller': user.newid,
        'customer': user.newid,
        'broker': user.newid,
    }
    pay_hash = services.hep_pay(order)
    pay_info = {
        'dapp_id': settings.HEP_ID,
        'action': settings.ACTION_PAY,
        'pay_hash': pay_hash
    }
    return http.JsonSuccessResponse(data=pay_info)


def request_pay_h5(request):
    login_id = request.session['uuid']
    user = HepProfileModel.objects.filter(uuid=login_id).first()
    newid = user.newid
    pay_session_id = uuid.uuid4().hex
    request.session['pay_id'] = pay_session_id
    pay_model = LoginModel()
    pay_model.login_id = pay_session_id
    pay_model.save()
    if not newid:
        body = json.loads(request.body)
        newid = body.get('newid')
    pay_params = {
        'uuid': pay_session_id,
        'action': settings.ACTION_PAY,
        'description': 'Pay description',
        'price_currency': 'NEW',
        'total_price': "1",
        'order_number': uuid.uuid4().hex,
        'seller': newid,
        'customer': newid,
        'broker': newid,
    }
    pay_params = _get_client_params(pay_params)
    return http.JsonSuccessResponse(data=pay_params)


def receive_profile(request):
    body = json.loads(request.body)
    profile_model = HepProfileModel()
    profile_model.uuid = body.get('uuid')
    if not profile_model.uuid:
        profile_model.uuid = request.session.get('uuid')
    profile_model.signature = body.get('signature')
    profile_model.newid = body.get('newid')
    profile_model.name = body.get('name')
    profile_model.avatar = body.get('avatar')
    profile_model.address = body.get('address')
    profile_model.cellphone = body.get('cellphone')
    profile_model.save()
    login_model = LoginModel.objects.filter(login_id=profile_model.uuid).first()
    if login_model:
        login_model.status = codes.StatusCode.AVAILABLE.value
        login_model.save()
    return http.JsonSuccessResponse(data=request.POST)


def receive_pay(request):
    pay_model = PayModel()
    pay_model.txid = request.POST.get('txid')
    if pay_model.txid:
        print(request.POST)
        pay_model.uuid = request.POST.get('uuid')
    else:
        body = json.loads(request.body)
        print(body)
        pay_model.txid = body.get('txid')
        pay_model.uuid = body.get('uuid')
    pay_model.save()
    login_model = LoginModel.objects.filter(login_id=pay_model.uuid).first()
    if login_model:
        login_model.status = codes.StatusCode.AVAILABLE.value
        login_model.save()
    return http.JsonSuccessResponse()


def query_pay(request):
    pay_model = LoginModel.objects.filter(login_id=request.session.get('pay_id')).first()
    if not pay_model:
        return http.JsonErrorResponse(error_message="no login model")
    if pay_model.status == codes.StatusCode.AVAILABLE.value:
        return http.JsonSuccessResponse()
    else:
        return http.JsonErrorResponse(error_message="error status")


def show_place_order(request):
    order = {
        "ordername": "芒果",
        "ordernumber": uuid.uuid4().hex,
        "price_currency": "NEW",
        "total_price": "100",
        "order_img": "https://newton-dapp-store.oss-cn-beijing.aliyuncs.com/banner1559375214.png"
    }
    return render(request, "demo/placeorder.html", {'order': order})


def request_proof(request):
    proof_session_id = uuid.uuid4().hex
    login_id = request.session['uuid']
    user = HepProfileModel.objects.filter(uuid=login_id).first()
    request.session['proof_id'] = proof_session_id
    login_model = LoginModel()
    login_model.login_id = proof_session_id
    login_model.save()
    # todo: add proof field.
    params = {
        'uuid': proof_session_id,
        'order': {
            'proof_type': 'order',
            'description': 'goods description',
            'price_currency': 'NEW',
            'total_price': '100',
            'order_number': uuid.uuid4().hex,
            'order_items': [
                {
                    'order_item_number': uuid.uuid4().hex,
                    'price': '12.2',
                    'price_currency': 'NEW',
                    'ordered_item': {
                        'name': '你好',
                        'thing_type': 'product',
                        'thing_id': uuid.uuid4().hex,
                    },
                    'order_item_quantity': 1
                }
            ],
            'seller': user.newid,
            'customer': user.newid,
            'broker': user.newid,
        }
    }
    proof_hash = services.hep_proof(params)
    pay_info = {
        'dapp_id': settings.HEP_ID,
        'action': settings.ACTION_PROOF_SUBMIT,
        'proof_hash': proof_hash
    }
    return http.JsonSuccessResponse(data=pay_info)


def get_proof_hash(request):
    os = request.POST.get('os')
    if not os:
        body = json.loads(request.body)
        os = body.get('os')
    newid = request.POST.get('newid')
    if not newid:
        body = json.loads(request.body)
        newid = body.get('newid')
    proof_session_id = uuid.uuid4().hex
    request.session['proof_id'] = proof_session_id
    login_model = LoginModel()
    login_model.login_id = proof_session_id
    login_model.save()
    params = {
        'uuid': proof_session_id,
        'order': {
            'proof_type': 'order',
            'description': 'goods description',
            'price_currency': 'NEW',
            'total_price': '100',
            'order_number': uuid.uuid4().hex,
            'order_items': [
                {
                    'order_item_number': uuid.uuid4().hex,
                    'price': '12.2',
                    'price_currency': 'NEW',
                    'ordered_item': {
                        'name': '你好',
                        'thing_type': 'product',
                        'thing_id': uuid.uuid4().hex,
                    },
                    'order_item_quantity': 1
                }
            ],
            'seller': newid,
            'customer': newid,
            'broker': newid,
        }
    }
    proof_hash = services.hep_proof(params)
    client_params = {
        'action': settings.ACTION_PROOF_SUBMIT,
        'proof_hash': proof_hash,
        'uuid': proof_session_id
    }
    client_params = _get_client_params(client_params, os)
    return http.JsonSuccessResponse(data=client_params)


def get_client_login(request):
    os = request.POST.get('os')
    if not os:
        body = json.loads(request.body)
        os = body.get('os')
    login_params = {
        'action': settings.ACTION_LOGIN,
        'scope': 2,
        'memo': 'Demo Request Login'
    }
    login_params = _get_client_params(login_params, os)
    return http.JsonSuccessResponse(data=login_params)


def get_client_pay(request):
    os = request.POST.get('os')
    if not os:
        body = json.loads(request.body)
        os = body.get('os')
    newid = request.POST.get('newid')
    if not newid:
        body = json.loads(request.body)
        newid = body.get('newid')
    pay_params = {
        'action': settings.ACTION_PAY,
        'description': 'Pay description',
        'price_currency': 'NEW',
        'total_price': "1",
        'order_number': uuid.uuid4().hex,
        'seller': newid,
        'customer': newid,
        'broker': newid,
    }
    pay_params = _get_client_params(pay_params, os)
    return http.JsonSuccessResponse(data=pay_params)


def request_login_h5(request):
    try:
        login_session_id = uuid.uuid4().hex
        request.session['uuid'] = login_session_id
        login_model = LoginModel()
        login_model.login_id = login_session_id
        login_params = {
            'action': settings.ACTION_LOGIN,
            'scope': 2,
            'memo': 'Demo Request Login',
            'uuid': login_session_id,
        }
        login_params = _get_client_params(login_params)
        return http.JsonSuccessResponse(data=login_params)
    except Exception as e:
        print(str(e))
        return http.JsonErrorResponse()


def request_proof_h5(request):
    proof_session_id = uuid.uuid4().hex
    login_id = request.session['uuid']
    user = HepProfileModel.objects.filter(uuid=login_id).first()
    request.session['proof_id'] = proof_session_id
    login_model = LoginModel()
    login_model.login_id = proof_session_id
    login_model.save()
    # todo: add proof field.
    params = {
        'uuid': proof_session_id,
        'order': {
            'proof_type': 'order',
            'description': 'goods description',
            'price_currency': 'NEW',
            'total_price': '100',
            'order_number': uuid.uuid4().hex,
            'order_items': [
                {
                    'order_item_number': uuid.uuid4().hex,
                    'price': '12.2',
                    'price_currency': 'NEW',
                    'ordered_item': {
                        'name': '你好',
                        'thing_type': 'product',
                        'thing_id': uuid.uuid4().hex,
                    },
                    'order_item_quantity': 1
                }
            ],
            'seller': user.newid,
            'customer': user.newid,
            'broker': user.newid,
        }
    }
    proof_hash = services.hep_proof(params)
    client_params = {
        'uuid': proof_session_id,
        'action': settings.ACTION_PROOF_SUBMIT,
        'proof_hash': proof_hash
    }
    client_params = _get_client_params(client_params)
    return http.JsonSuccessResponse(data=client_params)


def query_proof(request):
    proof_model = LoginModel.objects.filter(login_id=request.session.get('proof_id')).first()
    if not proof_model:
        return http.JsonErrorResponse(error_message="no login model")
    if proof_model.status == codes.StatusCode.AVAILABLE.value:
        return http.JsonSuccessResponse()
    else:
        return http.JsonErrorResponse(error_message="error status")


def receive_proof(request):
    proof_model = ProofModel()
    proof_model.uuid = request.POST.get('uuid')
    if not proof_model.uuid:
        body = json.loads(request.body)
        proof_model.uuid = body.get('uuid')
    proof_model.txid = uuid.uuid4().hex
    proof_model.save()
    login_model = LoginModel.objects.filter(login_id=proof_model.uuid).first()
    if login_model:
        login_model.status = codes.StatusCode.AVAILABLE.value
        login_model.save()
    return http.JsonSuccessResponse()


def post_profile(request):
    body = json.loads(request.body)
    profile_model = HepProfileModel()
    profile_model.uuid = uuid.uuid4().hex
    profile_model.signature = body.get('signature')
    profile_model.newid = body.get('newid')
    profile_model.name = body.get('name')
    profile_model.avatar = body.get('avatar')
    profile_model.address = body.get('address')
    profile_model.cellphone = body.get('cellphone')
    profile_model.save()
    request.session['uuid'] = profile_model.uuid
    return http.JsonSuccessResponse()


def _get_client_params(data, os=None):
    if os == "android":
        dapp_id = settings.DAPP_ID_ANDROID
        private_key_path = settings.DAPP_ID_ANDROID_PRIVATE_PATH
    elif os == "ios":
        dapp_id = settings.DAPP_ID_IOS
        private_key_path = settings.DAPP_ID_IOS_PRIVATE_PATH
    else:
        dapp_id = settings.HEP_ID
        private_key_path = settings.PRIVATE_KEY_PATH
    params = {
        'dapp_id': dapp_id,
        'protocol': settings.HEP_PROTOCOL,
        'version': settings.HEP_PROTOCOL_VERSION,
        'ts': int(datetime.datetime.now().timestamp()),
        'nonce': uuid.uuid4().hex,
        'sign_type': settings.SIGN_TYPE,
    }
    data.update(params)
    message = utils.generate_signature_base_string(data, "&")
    r, s = utils.sign_secp256r1(message, private_key_path)
    if r.startswith('0x'):
        r = r.replace('0x', '')
    if s.startswith('0x'):
        s = s.replace('0x', '')
    if len(r) < 64:
        x = 64 - len(r)
        r = '0' * x + r
    if len(s) < 64:
        y = 64 - len(s)
        s = '0' * y + s
    data['signature'] = '0x' + r + s
    return data




