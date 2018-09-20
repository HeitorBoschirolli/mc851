from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^status_boleto=(?P<pk>\d+)', views.status_boleto, name='status_boleto'),
    url(r'^input=(?P<pk>\d+)', views.input,  name='input'),
    url(r'^status_boleto', views.status_boleto, name='status_boleto'),
]
