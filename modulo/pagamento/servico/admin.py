from django.contrib import admin

from .models import *

admin.site.register(Pedido)
admin.site.register(Cartao)
admin.site.register(Boleto)
admin.site.register(Banco)
