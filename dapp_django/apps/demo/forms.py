# -*- coding:utf-8 -*-
__author__ = 'weixuefeng@lubangame.com'
__version__ = ''
__doc__ = ''

from django import forms
from .models import HepProfileModel


class HepProfileForm(forms.ModelForm):

    class Meta:
        model = HepProfileModel
        fields = (
            'uuid',
            'cellphone',
            'name',
            'newid'
        )
