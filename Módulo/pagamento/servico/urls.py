# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^compra_com_cartao/$', views.CompraComCartao, name='Compra Cartao'),
    url(r'^pagamento_boleto', views.pagamento_boleto, name='pagamento_boleto'),
    url(r'^input=(?P<pk>\d+)', views.input,  name='input'),
    url(r'^status_boleto', views.status_boleto, name='status_boleto'),
    url(r'^feedback_pagamento_boleto', 
        views.feedback_pagamento_boleto, 
        name='feedback_pagamento_boleto'),
]
