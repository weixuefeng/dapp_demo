from django.db import models

from dapp_django.config import codes


class LoginModel(models.Model):
    login_id = models.CharField(max_length=128, db_index=True)
    status = models.IntegerField(default=codes.StatusCode.INVALID.value)

    class Meta:
        app_label = "demo"


class HepProfileModel(models.Model):
    uuid = models.CharField(max_length=128, db_index=True)
    signature = models.CharField(max_length=500, default='')
    sign_type = models.CharField(max_length=20, default='')

    country_code = models.CharField(max_length=10, default='')
    cellphone = models.CharField(max_length=128, default='')
    name = models.CharField(max_length=128, default='')
    newid = models.CharField(max_length=128, default='')
    avatar = models.CharField(max_length=500, default='')
    invite_code = models.CharField(max_length=10, default='')
    address = models.CharField(max_length=42, default='')

    class Meta:
        app_label = "demo"


class PayModel(models.Model):
    uuid = models.CharField(max_length=128, db_index=True)
    txid = models.CharField(max_length=128, db_index=True)


class ProofModel(models.Model):
    uuid = models.CharField(max_length=128, db_index=True)
    txid = models.CharField(max_length=128, db_index=True)
