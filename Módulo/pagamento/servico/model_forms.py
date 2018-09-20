# -*- coding: utf-8 -*-

from django import forms
from .models import *
# from .constant import *

class PagamentoForm(forms.Form):
    cpf_comprador = forms.CharField(label="CPF Comprador", max_length=50)
    valor_compra = forms.CharField(label="Valor", max_length=50)
    data_emissao = forms.DateField(label="Data de Emissão")
    cnpj_site = forms.CharField(label="CNPJ", max_length=50)

class PagamentoCartaoForm(PagamentoForm):
    # CARTAO
    num_cartao = forms.CharField(label="Numero do Cartão", max_length=50)
    cvv = forms.CharField(label="CVV", max_length=5)
    nome_cartao = forms.CharField(label="Nome no Cartão", max_length=50)
    data_vencimento_cartao_str = forms.DateField(label="Data de Vencimento")
    credito = forms.BooleanField(label="Crédito")
    num_parcelas = forms.IntegerField(label="Num. Parcelas")
    pedido = forms.IntegerField(label="Pedido")

class PagamentoBoletoForm(PagamentoForm):
    banco_gerador_boleto = forms.CharField(label="Banco", max_length=50)
    data_vencimento_boleto = forms.CharField(label="Data de Vencimento",
                                             max_length=50)
    endereco_fisico_site = forms.CharField(label="Endereco Empresa",
                                            max_length=100)