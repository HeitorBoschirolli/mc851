from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^teste', views.teste, name='teste'),
]