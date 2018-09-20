from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^pagamento_boleto', views.pagamento_boleto, name='pagamento_boleto'),
    url(r'^status_boleto', views.status_boleto, name='status_boleto'),
]
