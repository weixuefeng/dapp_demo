import datetime
import json
import uuid
import logging
logger = logging.getLogger(__name__)

from dapp_django.config import codes
from dapp_django.hep_service import services
from dapp_django.utils import http
from django.conf import settings
from django.shortcuts import render
from hep_rest_api import utils
from hep_rest_api.scenarios.proof import OrderProof, Order
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
        qr_code_str = services.hep_login(session_id)
        login = {'qr_str': qr_code_str,
                 'uuid': session_id
                 }
        request.session['uuid'] = session_id
        return render(request, "demo/hep_login.html", {'login': login})
    except Exception as e:
        logger.exception("request login error:%s" % str(e))
        return http.JsonErrorResponse()


def query_profile(request):
    try:
        login_model = LoginModel.objects.filter(login_id=request.session.get('uuid')).first()
        if not login_model:
            return http.JsonErrorResponse(error_message="no login model")
        if login_model.status == codes.StatusCode.AVAILABLE.value:
            return http.JsonSuccessResponse()
        else:
            return http.JsonErrorResponse(error_message="error status")
    except Exception as e:
        logger.exception("qurey profile error:%s" % str(e))
        return http.JsonErrorResponse()


def user_center(request):
    try:
        login_id = request.session['uuid']
        user = HepProfileModel.objects.filter(uuid=login_id).first()
        return render(request, "demo/user.html", {'user': user})
    except Exception as e:
        logger.exception("user center error:%s" % str(e))
        return http.JsonErrorResponse()


def show_order(request):
    try:
        order = {
            "ordername": "芒果",
            "ordernumber": uuid.uuid4().hex,
            "price_currency": "NEW",
            "total_price": "100",
            "order_img": "https://newton-dapp-store.oss-cn-beijing.aliyuncs.com/banner1559375214.png"
        }
        return render(request, "demo/orderlist.html", {'order': order})
    except Exception as e:
        logger.exception("show order error:%s" % str(e))
        return http.JsonErrorResponse()


def request_pay(request):
    try:
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
            'total_price': '0.01',
            'order_number': order_number,
            'seller': user.newid,
            'customer': user.newid,
            'broker': user.newid,
        }
        pay_qr_str = services.hep_pay(order)
        pay_info = {
            'pay_qr_str': pay_qr_str
        }
        return http.JsonSuccessResponse(data=pay_info)
    except Exception as e:
        logger.exception("query pay error:%s" % str(e))
        return http.JsonErrorResponse()


def request_pay_h5(request):
    try:
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
            'total_price': "0.01",
            'order_number': uuid.uuid4().hex,
            'seller': newid,
            'customer': newid,
            'broker': newid,
        }
        pay_params = _get_client_params(pay_params)
        return http.JsonSuccessResponse(data=pay_params)
    except Exception as e:
        logger.exception("request pay h5 error:%s" % str(e))
        return http.JsonErrorResponse()


def receive_profile(request):
    try:
        content_type = request.META.get('CONTENT_TYPE') or request.META.get['HTTP_CONTENT_TYPE']
        if content_type.find('application/json') > -1:
            data = json.loads(request.body)
            if data:
                request.POST = data
        body = request.POST
        logger.info(body)
        is_valid = services.verify_profile(body)
        if is_valid:
            profile_model = HepProfileModel()
            profile_model.uuid = body.get('uuid')
            if not profile_model.uuid:
                logger.error("no uuid")
                return http.JsonErrorResponse(error_message="no uuid")
            profile_model.signature = body.get('signature')
            profile_model.newid = body.get('newid')
            profile_model.name = body.get('name')
            profile_model.avatar = body.get('avatar')
            profile_model.address = body.get('address')
            profile_model.cellphone = body.get('cellphone')
            if not profile_model.cellphone:
                profile_model.cellphone = "scope is 1,no cellphone"
            if not profile_model.address:
                profile_model.address = "scope is 1,no address"
            profile_model.save()
            login_model = LoginModel.objects.filter(login_id=profile_model.uuid).first()
            if login_model:
                login_model.status = codes.StatusCode.AVAILABLE.value
                logger.info("update profile info status")
                login_model.save()
                return http.HttpResponse("OK")
            else:
                logger.error("no login id ")
                return http.JsonErrorResponse(error_message="no login id")
        else:
            logger.error("invalidate profile information")
            return http.JsonErrorResponse(error_message="invalidate profile information")
    except Exception as e:
        logger.exception("receive profile error:%s" % str(e))
        return http.JsonErrorResponse()


def receive_pay(request):
    try:
        content_type = request.META.get('CONTENT_TYPE') or request.META.get['HTTP_CONTENT_TYPE']
        if content_type.find('application/json') > -1:
            data = json.loads(request.body)
            if data:
                request.POST = data
        body = request.POST
        print("pay info:")
        print(body)
        pay_model = PayModel()
        pay_model.txid = body.get('txid')
        pay_model.uuid = body.get('uuid')
        pay_model.save()
        print("pay_id" + pay_model.uuid)
        login_model = LoginModel.objects.filter(login_id=pay_model.uuid).first()
        if login_model:
            login_model.status = codes.StatusCode.AVAILABLE.value
            login_model.save()
        return http.JsonSuccessResponse()
    except Exception as e:
        logger.exception("receive pay error:%s" % str(e))
        return http.JsonErrorResponse()


def query_pay(request):
    try:
        pay_model = LoginModel.objects.filter(login_id=request.session.get('pay_id')).first()
        print(request.session.get('pay_id'))
        if not pay_model:
            return http.JsonErrorResponse(error_message="no login model")
        if pay_model.status == codes.StatusCode.AVAILABLE.value:
            del request.session['pay_id']
            return http.JsonSuccessResponse()
        else:
            return http.JsonErrorResponse(error_message="error status")
    except Exception as e:
        logger.exception("query pay error:%s" % str(e))
        return http.JsonErrorResponse()


def show_place_order(request):
    try:
        order = {
            "ordername": "芒果",
            "ordernumber": uuid.uuid4().hex,
            "price_currency": "NEW",
            "total_price": "100",
            "order_img": "https://newton-dapp-store.oss-cn-beijing.aliyuncs.com/banner1559375214.png"
        }
        return render(request, "demo/placeorder.html", {'order': order})
    except Exception as e:
        logger.exception("show place order error:%s" % str(e))
        return http.JsonErrorResponse()


def request_proof(request):
    try:
        proof_session_id = uuid.uuid4().hex
        login_id = request.session['uuid']
        user = HepProfileModel.objects.filter(uuid=login_id).first()
        request.session['proof_id'] = proof_session_id
        login_model = LoginModel()
        login_model.login_id = proof_session_id
        login_model.save()
        # todo: add proof field.
        pay_model = PayModel.objects.last()
        txid = pay_model.txid
        order_content = _get_proof_content(user.newid)
        proof_qr_str = services.hep_proof(order_content.to_dict(), proof_session_id)
        pay_info = {
            'proof_qr_str': proof_qr_str,
        }
        return http.JsonSuccessResponse(data=pay_info)
    except Exception as e:
        logger.exception("request proof error:%s" % str(e))
        return http.JsonErrorResponse()


def get_proof_hash(request):
    try:
        os = request.POST.get('os')
        if not os:
            body = json.loads(request.body)
            os = body.get('os')
        newid = request.POST.get('newid')
        if not newid:
            body = json.loads(request.body)
            newid = body.get('newid')
        # todo: add proof field.
        pay_model = PayModel.objects.last()
        txid = pay_model.txid
        proof_session_id = uuid.uuid4().hex
        order_content = _get_proof_content(newid)
        proof_hash = services.get_proof_hash(order_content.to_dict(), proof_session_id, os)
        client_params = {
            'action': settings.ACTION_PROOF_SUBMIT,
            'proof_hash': proof_hash,
            'uuid': proof_session_id
        }
        client_params = _get_client_params(client_params, os)
        return http.JsonSuccessResponse(data=client_params)
    except Exception as e:
        logger.exception("get proof hash error:%s" % str(e))
        return http.JsonErrorResponse(error_message=str(e))


def _get_proof_content(newid):
    order = Order(uuid.uuid4().hex, "deacription1", "0.04", "CNY", newid, newid)
    order.add_order_item(uuid.uuid4().hex, 1, "0.01", "CNY", "pingguo", uuid.uuid4().hex)
    order.add_order_item(uuid.uuid4().hex, 2, "0.01", "CNY", "xiangjiao", uuid.uuid4().hex)
    order.add_order_item(uuid.uuid4().hex, 2, "0.01", "CNY", "li", uuid.uuid4().hex)
    order.add_order_item(uuid.uuid4().hex, 2, "0.01", "CNY", "你好", uuid.uuid4().hex)

    order1 = Order(uuid.uuid4().hex, "description2", "0.04", "CNY", newid, newid)
    order1.add_order_item(uuid.uuid4().hex, 1, "0.01", "CNY", "order2", uuid.uuid4().hex)
    order1.add_order_item(uuid.uuid4().hex, 2, "0.01", "CNY", "order2xiangjiao", uuid.uuid4().hex)
    order1.add_order_item(uuid.uuid4().hex, 2, "0.01", "CNY", "order2li", uuid.uuid4().hex)
    order1.add_order_item(uuid.uuid4().hex, 2, "0.01", "CNY", "order2你好", uuid.uuid4().hex)

    order_content = OrderProof("0.08", "CNY", newid)
    order_content.add_order(order.to_dict())
    order_content.add_order(order1.to_dict())
    return order_content


def get_client_login(request):
    try:
        os = request.POST.get('os')
        if not os:
            body = json.loads(request.body)
            os = body.get('os')
        login_params = {
            'action': settings.ACTION_LOGIN,
            'scope': 2,
            'memo': 'Demo Request Login',
            'uuid': uuid.uuid4().hex
        }
        login_params = _get_client_params(login_params, os)
        return http.JsonSuccessResponse(data=login_params)
    except Exception as e:
        logger.exception("get client login error:%s" % str(e))
        return http.JsonErrorResponse()


def get_client_pay(request):
    try:
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
            'uuid': uuid.uuid4().hex
        }
        pay_params = _get_client_params(pay_params, os)
        return http.JsonSuccessResponse(data=pay_params)
    except Exception as e:
        logger.exception("get client pay error:%s" % str(e))
        return http.JsonErrorResponse()


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
        logger.exception("get client pay error:%s" % str(e))
        return http.JsonErrorResponse()


def request_proof_h5(request):
    try:
        proof_session_id = uuid.uuid4().hex
        login_id = request.session['uuid']
        user = HepProfileModel.objects.filter(uuid=login_id).first()
        request.session['proof_id'] = proof_session_id
        login_model = LoginModel()
        login_model.login_id = proof_session_id
        login_model.save()
        # todo: add proof field.
        pay_model = PayModel.objects.last()
        txid = pay_model.txid
        order_content = _get_proof_content(user.newid)
        print(order_content.to_dict())
        proof_hash = services.get_proof_hash(order_content.to_dict(), proof_session_id)
        client_params = {
            'uuid': proof_session_id,
            'action': settings.ACTION_PROOF_SUBMIT,
            'proof_hash': proof_hash
        }
        client_params = _get_client_params(client_params)
        return http.JsonSuccessResponse(data=client_params)
    except Exception as e:
        logger.exception("request proof error:%s" % str(e))
        return http.JsonErrorResponse()


def query_proof(request):
    try:
        proof_model = LoginModel.objects.filter(login_id=request.session.get('proof_id')).first()
        print(proof_model)
        if not proof_model:
            return http.JsonErrorResponse(error_message="no login model")
        if proof_model.status == codes.StatusCode.AVAILABLE.value:
            del request.session['proof_id']
            return http.JsonSuccessResponse()
        else:
            return http.JsonErrorResponse(error_message="error status")
    except Exception as e:
        logger.exception("query proof error:%s" % str(e))
        return http.JsonErrorResponse()


def receive_proof(request):
    try:
        body = _get_body(request)
        proof_model = ProofModel()
        proof_model.uuid = body.get('uuid')
        proof_status = services.verify_proof(body)
        if proof_status:
            print(proof_status.proof_status)
            print(proof_status.proof_hash)
            proof_model.txid = uuid.uuid4().hex
            proof_model.save()
            login_model = LoginModel.objects.filter(login_id=proof_model.uuid).first()
            if login_model:
                login_model.status = codes.StatusCode.AVAILABLE.value
                login_model.save()
            return http.JsonSuccessResponse()
        else:
            return http.JsonErrorResponse(error_message="verify_proof error")
    except Exception as e:
        logger.exception("receive proof error:%s" % str(e))
        return http.JsonErrorResponse()


def post_profile(request):
    try:
        body = request.POST
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
    except Exception as e:
        logger.exception("post profile error:%s" % str(e))
        return http.JsonErrorResponse()


def _get_client_params(data, os=None):
    if os == "android":
        dapp_id = settings.DAPP_ID_ANDROID
        private_key_path = settings.DAPP_ID_ANDROID_PRIVATE_PATH
    elif os == "ios":
        dapp_id = settings.DAPP_ID_ANDROID
        private_key_path = settings.DAPP_ID_ANDROID_PRIVATE_PATH
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


def _get_body(request):
    content_type = request.META.get('CONTENT_TYPE') or request.META.get['HTTP_CONTENT_TYPE']
    if content_type.find('application/json') > -1:
        data = json.loads(request.body)
        if data:
            request.POST = data
    body = request.POST
    return body


def get_client_sign_message(request):
    try:
        body = _get_body(request)
        message = body.get('message')
        sign_message_data = {
            'message': message,
            'action': settings.ACTION_SIGN_MESSAGE,
        }
        sign_message_data = _get_client_params(sign_message_data)
        return http.JsonSuccessResponse(data=sign_message_data)
    except Exception as e:
        logger.exception("get_client_sign_message error:%s" % str(e))
        return http.JsonErrorResponse()


def get_client_sign_transaction(request):
    try:
        body = _get_body(request)
        sign_transaction_data = {
            'action': settings.ACTION_SIGN_TRANSACTION,
            'amount': body.get('amount'),
            'from': body.get('from'),
            'to': body.get('to'),
            'transaction_count': body.get('transaction_count'),
            'gas_price': body.get('gas_price'),
            'gas_limit': body.get('gas_limit'),
            'data': body.get('data')
        }
        sign_transaction_data = _get_client_params(sign_transaction_data)
        return http.JsonSuccessResponse(data=sign_transaction_data)
    except Exception as e:
        logger.exception("get_client_sign_transaction error:%s" % str(e))
        return http.JsonErrorResponse()





