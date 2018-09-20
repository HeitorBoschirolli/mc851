from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^compra_com_cartao/$', views.CompraComCartao, name='Compra Cartao'),
    url(r'^input=(?P<pk>\d+)', views.input,  name='input'),
    url(r'^status_boleto', views.status_boleto, name='status_boleto'),
]
