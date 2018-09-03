from django import forms
from .models import *


    

class PagamentoForm(forms.Form):
    nome_cartao = forms.CharField(label="Nome no Cartão", max_length=50)
    numero_cartao = forms.CharField(label="Número do Cartão", max_length=50)
    CVV = forms.CharField(label="CVV", max_length=50)
    data_vencimento_cartao = forms.DateField(widget=forms.TextInput(attrs={'id':'datetimepicker1'}))

    