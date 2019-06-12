# -*- coding:utf-8 -*-
__author__ = 'weixuefeng@lubangame.com'
__version__ = ''
__doc__ = ''

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.3, 2.4 fallback.

from django.http import HttpResponse
import dapp_django.utils.coder as coder
import json as simplejson
from django.conf import settings
from dapp_django.config import codes


class JsonResponse(HttpResponse):
    """
    Http Response based on ajax
    The default mime type is json and the encoding is utf8.
    """
    def __init__(self, data, encoding="utf-8", content_type='application/json'):
        super(JsonResponse, self).__init__(simplejson.dumps(coder.uni_str(data, encoding)), content_type=content_type)


class JsonErrorResponse(JsonResponse):
    def __init__(self, error_code=None, error_message=None, data={}):
        if not error_code:
            error_code = codes.ErrorCode.FAIL.value
        responseData = {}
        responseData['error_code'] = error_code
        responseData['result'] = data
        if error_message:
            responseData['error_message'] = error_message
        else:
            if settings.ERROR_CODE_LABEL[error_code]:
                responseData['error_message'] = str(settings.ERROR_CODE_LABEL[error_code])
        super(JsonErrorResponse, self).__init__(responseData)


class JsonSuccessResponse(JsonResponse):
    def __init__(self, data={}):
        responseData = {}
        responseData['error_code'] = codes.ErrorCode.SUCCESS.value
        responseData['result'] = data
        super(JsonSuccessResponse, self).__init__(responseData)


class JsonUnauthErrorResponse(JsonResponse):
    def __init__(self, error_code=None, error_message=None):
        if not error_code:
            error_code = codes.ErrorCode.UNAUTH.value
        responseData = {}
        responseData['error_code'] = error_code
        if error_message:
            responseData['error_message'] = error_message
        super(JsonUnauthErrorResponse, self).__init__(responseData)


def parse_ip_address(address):
    ip_address_list = address.split(',')
    if len(ip_address_list) > 1:
        for ip_address in ip_address_list:
            ip_address = ip_address.strip()
            if (not ip_address.startswith('10.')) and (not ip_address.startswith('192.')) and (not ip_address.startswith('172.')):
                return ip_address
    return address.strip()


def get_client_ip(request):
    # Retrieve the x-forwarded-for header from proxy
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if not ip_address:
        ip_address = request.META['REMOTE_ADDR']
        return ip_address.strip()
    else:
        return parse_ip_address(ip_address)
