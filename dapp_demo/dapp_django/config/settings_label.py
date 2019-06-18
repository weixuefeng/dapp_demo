# -*- coding:utf-8 -*-
__author__ = 'weixuefeng@lubangame.com'
__version__ = ''
__doc__ = ''
from . import codes


ERROR_CODE_LABEL = {
    codes.ErrorCode.FAIL.value: 'Operation failed',
    codes.ErrorCode.SUCCESS.value: 'Operation success',
    codes.ErrorCode.UNAUTH.value: 'Session expired, login please!',
    codes.ErrorCode.SIGN_ERROR.value: 'Signature error',
    codes.ErrorCode.INVALID_PARAMS.value: 'Parameters error',
    codes.ErrorCode.UPGRADE.value: 'Your app version is too old, please upgrade',
    codes.ErrorCode.BLOCK_USER.value: 'Your account has been locked, please contact customer service',
}
