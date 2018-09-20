from django import forms
from .models import *
# from .constant import *


class PagamentoForm(forms.Form):
    cpf_comprador = forms.CharField(label="CPF Comprador", 
                                    max_length=50)
    valor_compra = forms.CharField(label="Valor", max_length=50)
    banco_gerador_boleto = forms.CharField(label="Banco", max_length=50)
    cnpj_site = forms.CharField(label="CNPJ", max_length=50)
    data_vencimento_boleto = forms.CharField(label="Data de Vencimento",
                                             max_length=50)
    endereco_fisico_site = forms.CharField(label="Endereco Empresa",
                                            max_length=100)