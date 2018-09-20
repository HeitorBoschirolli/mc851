from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^compra_com_cartao/$', views.CompraComCartao, name='Compra Cartao'),
]
