# -*- coding:utf-8 -*-
__author__ = 'weixuefeng@lubangame.com'
__version__ = ''
__doc__ = ''

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('user/login', views.request_login, name="request_login"),
    path('user/query', views.query_profile, name="query_profile"),
    path('user', views.user_center, name="user_center"),

    path('receive/pay/', views.receive_pay, name="receive_pay"),
    path('receive/proof/', views.receive_proof, name="receive_proof"),
    path('receive/profile/', views.receive_profile, name="receive_profile"),

    path('order/', views.show_order, name="show_order"),
    path('request/pay', views.request_pay, name="request_pay"),
    path('query/pay/', views.query_pay, name="query_pay"),

    path('placeorder/', views.show_place_order, name="show_place_order"),
    path('request/proof/', views.request_proof, name="request_proof"),
    path('query/proof/', views.query_proof, name="query_proof"),
]