from django.contrib import admin
from .models import Pedido, Cartao, Boleto, Cliente

# Register your models here.
admin.site.register(Pedido)
admin.site.register(Cartao)
admin.site.register(Boleto)
admin.site.register(Cliente)