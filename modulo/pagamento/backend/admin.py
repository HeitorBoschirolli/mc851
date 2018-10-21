from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Produtos)
admin.site.register(Carrinho)
admin.site.register(Usuario)
admin.site.register(Pedidos)
admin.site.register(Produtos_no_Carrinho)
