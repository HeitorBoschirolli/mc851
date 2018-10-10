from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^teste', views.teste, name='teste'),
    url(r'^cadastra_cliente', views.cadastra_cliente, name='cadastra_cliente'),
]