from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'pagamento'

urlpatterns = [
    path('id_pagamento=<int:pk_cliente>&id_pedido=<int:pk_pedido>/', views.get_pagamento, name='pagamento'),
    path('resposta_pagamento/', views.resposta_pagamento, name='resposta'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('falha/', views.falha, name='falha'),
    path('', views.index, name='index'),
]
