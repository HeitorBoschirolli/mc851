# -*- coding: utf-8 -*-
from django import forms
from .models import *
from . import constant

class PedidoForm(forms.Form):
    pedido_id = forms.IntegerField(label = "ID do Pedido")

class PrimaryKey(forms.Form):
    pk1 = models.CharField(max_length= 1)

class PagamentoForm(forms.Form):
    cpf_comprador = forms.CharField(label="CPF Comprador", max_length=50)
    valor_compra = forms.CharField(label="Valor", max_length=50)
    data_emissao_pedido = forms.DateField(label="Data de Emissão")
    cnpj_site = forms.CharField(label="CNPJ", max_length=50)

class PagamentoCartaoForm(PagamentoForm):
    # CARTAO
    numero_cartao = forms.CharField(label="Numero do Cartão", max_length=50, required=True)
    cvv_cartao = forms.CharField(label="CVV", max_length=5)
    nome_cartao = forms.CharField(label="Nome no Cartão", max_length=50)
    data_vencimento_cartao = forms.DateField(label="Data de Vencimento")
    credito = forms.IntegerField(label="Crédito")
    num_parcelas = forms.IntegerField(label="Numa. Parcelas")

    def __init__(self, *args, **kwargs):
        super(PagamentoCartaoForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False


class PagamentoBoletoForm(PagamentoForm):
    banco_gerador_boleto = forms.CharField(label="Banco", max_length=50)
    data_vencimento_boleto = forms.CharField(label="Data de Vencimento",
                                             max_length=50)
    endereco_fisico_site = forms.CharField(label="Endereco Empresa",
                                            max_length=100)
