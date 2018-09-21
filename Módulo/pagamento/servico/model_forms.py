from django import forms
from .models import *
from . import constant

class PedidoForm(forms.Form):
    pedido_id = forms.IntegerField(label = "ID do Pedido")
