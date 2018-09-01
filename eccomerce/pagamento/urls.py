from django.urls import path

from . import views

urlpatterns = [
    path('<int:cpf>/', views.get_pagamento, name='pedido'),
    path('', views.index, name='index'),
]
