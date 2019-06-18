# -*- coding:utf-8 -*-
__author__ = 'weixuefeng@lubangame.com'
__version__ = ''
__doc__ = ''
from enum import Enum


class ErrorCode(Enum):
    FAIL = 0
    SUCCESS = 1
    UNAUTH = 2
    SIGN_ERROR = 3
    INVALID_PARAMS = 4
    MAINTAIN = 5
    UPGRADE = 6
    # common
    INVALID_AUTH = 100
    WRONG_PASSWORD = 101
    WRONG_CELLPHONE = 102
    INFORMAT_PASSWORD_CELLPHONE = 103
    BLOCK_USER = 104
    UNIT_USER_NOT_EXIST = 105
    WRONG_EMAIL = 106


class Language(Enum):
    CHINESE = 1
    ENGLISH = 2


class StatusCode(Enum):
    USER_DELETE = 0
    AVAILABLE = 1
    CANDIDATE = 2
    RELEASE = 3
    INTERVIEW = 4
    OFFER = 5
    CONTRACT = 6
    FIRE = 7
    CANCEL = 8
    CLOSE = 9
    REJECT = 10
    READ = 11
    INVALID = 12
    BLOCK = 13
    AUTO_CANCEL = 14


class UserFrom(Enum):
    DIRECT_REGISTER = 1
    QQ = 2
    WEIBO = 3
    WEIXIN = 4


class UserType(Enum):
    NORMAL = 1


class Gender(Enum):
    MALE = 1
    FEMALE = 2
    UNKNOWN = 3


class MembershipType(Enum):
    NORMAL = 1
    GOLD = 2
    PT = 3


class JobType(Enum):
    UNKNOWN = 1
    WORKING = 2
    NOWORK = 3


class EmailType(Enum):
    REGISTER = 1
    RESET = 2
    TEXCHANGE_CONFIRM_KYC = 3
    TEXCHANGE_REJECT_KYC = 4
    TEXCHANGE_INVITE_NOTIFY = 5
    TEXCHANGE_ASSIGN_AMOUNT_NOTIFY = 6
    TEXCHANGE_RECEIVE_NOTIFY = 7


class ConstructionType(Enum):
    UNKNOWN = 1
    UI = 2
    PROGRAM = 3


class KYCStatus(Enum):
    CANDIDATE = 1
    PASS_KYC = 2
    REJECT = 3
    DENY = 4


KYC_STATUS_CANDIDATE_VALUE = KYCStatus.CANDIDATE.value
KYC_STATUS_PASS_KYC_VALUE = KYCStatus.PASS_KYC.value
KYC_STATUS_REJECT_VALUE = KYCStatus.REJECT.value
KYC_STATUS_DENY_VALUE = KYCStatus.DENY.value


class TokenExchangeStatus(Enum):
    INVITE = 1
    SEND_INVITE_NOTIFY = 2
    APPLY_AMOUNT = 3
    DISTRIBUTE_AMOUNT = 4
    CONFIRM_AMOUT = 5
    SEND_TRANSFER_NOTIFY = 6


TOKEN_EXCHANGE_STATUS_INVITE_VALUE = TokenExchangeStatus.INVITE.value
TOKEN_EXCHANGE_STATUS_SEND_INVITE_NOTIFY_VALUE = TokenExchangeStatus.SEND_INVITE_NOTIFY.value
TOKEN_EXCHANGE_STATUS_APPLY_AMOUNT_VALUE = TokenExchangeStatus.APPLY_AMOUNT.value
TOKEN_EXCHANGE_STATUS_DISTRIBUTE_AMOUNT_VALUE = TokenExchangeStatus.DISTRIBUTE_AMOUNT.value
TOKEN_EXCHANGE_STATUS_CONFIRM_AMOUT_VALUE = TokenExchangeStatus.CONFIRM_AMOUT.value
TOKEN_EXCHANGE_STATUS_SEND_TRANSFER_NOTIFY_VALUE = TokenExchangeStatus.SEND_TRANSFER_NOTIFY.value


class FundPhase(Enum):
    PRIVATE = 1
    PUBLIC = 2


FUNDPHASE_PRIVATE_VALUE = FundPhase.PRIVATE.value
FUNDPHASE_PUBLIC_VALUE = FundPhase.PUBLIC.value


class CurrencyType(Enum):
    BTC = 1
    ELA = 2


class AdminActionType(Enum):
    PASS_KYC = 1
    REJECT_KYC = 2
    DENY_KYC = 3
    INVITE = 4
    SEND_INVITE = 5
    ASSIGN_AMOUNT = 6
    CONFIRM_AMOUNT = 7
    SEND_CONFIRM_EMAIL = 8


class IDType(Enum):
    ID_CARD = 1
    PASSPORT = 2
    DRIVERS_LICENSE = 3


class EstablishNodeType(Enum):
    YES = 1
    NO = 2


class NodeType(Enum):
    UNKNOWN = 0
    FULL_NODE = 1
    MEDIA_NODE = 2
    TECH_NODE = 3
    OPERATION_NODE = 4


class KYCType(Enum):
    INDIVIDUAL = 1
    ORGANIZATION = 2


KYC_TYPE_INDIVIDUAL_VALUE = KYCType.INDIVIDUAL.value
KYC_TYPE_ORGANIZATION_VALUE = KYCType.ORGANIZATION.value


class RelationshipWithEmergency(Enum):
    KINSHIP = 1
    FRIENDSHIP = 2
    COLLEAGUE = 3


class UserCenterActivePage(Enum):
    KYCACTIVE = 1
    TOKENEXCHANGEACTIVE = 2


class SubscriptionEmailType(Enum):
    AVAILABLE = 0
    SPAM = 1


class EntryLanguage(Enum):
    CHINESE = 0
    ENGLISH = 1
    KOREAN = 2
    JAPANESE = 3
    RUSSIAN = 4
    TURKISH = 5
    SPANISH = 6
    FRENCH = 7
    GERMAN = 8
    ARABIC = 9
    NETHERLAND = 10
    FINNISH = 11
    INDONESIAN = 12
    ITALY = 13
    THAILAND = 14
    PORTUGUESE = 15
    VIETNAMESE = 16
    ROMANIA = 17
