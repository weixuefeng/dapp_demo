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

    path('request/login/h5/', views.request_login_h5, name="request_login_h5"),
    path('request/pay/h5/', views.request_pay_h5, name="request_pay_h5"),
    path('request/proof/h5/', views.request_proof_h5, name="request_proof_h5"),

    path('post/profile/', views.post_profile, name="post_profile"),

    path('get/client/proof/', views.get_proof_hash, name="get_proof_hash"),
    path('get/client/login/', views.get_client_login, name="get_client_login"),
    path('get/client/pay/', views.get_client_pay, name="get_client_pay"),
    path('get/client/sign/message/', views.get_client_sign_message, name="get_client_sign_message"),
    path('get/client/sign/transaction/', views.get_client_sign_transaction, name="get_client_sign_message")
]