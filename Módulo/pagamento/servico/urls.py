from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^busca_pedido/', views.busca_pedido, name='busca_pedido'),
    url(r'^busca_pagamento/resultado/', views.busca_pedido_resultado, name='busca_pedido_resultado'),
]
