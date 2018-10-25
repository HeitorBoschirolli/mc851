# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^pagamento_cartao', views.pagamento_cartao, name='Compra Cartao'),
    url(r'^pagamento_boleto', views.pagamento_boleto, name='pagamento_boleto'),
    url(r'^status_boleto', views.status_boleto, name='status_boleto'),
    url(r'^busca_pedido', views.busca_pedido, name='busca_pedido'),
    url(r'^teste', views.teste, name='teste'),
    url(r'^simula_pagamento_boleto/(?P<numero_boleto>[0-9]+)', views.simula_pagamento_boleto, name='simula_pagamento_boleto'),
]
