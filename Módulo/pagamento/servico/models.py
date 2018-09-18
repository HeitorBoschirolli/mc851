from django.db import models
import datetime
from django.utils import timezone
from . import constant

class Pedido(models.Model):
    cpf_cliente = models.CharField(max_length = constant.CPF_CLIENTE_LENGHT)
    cnpj_empresa = models.CharField(max_length = constant.CNPJ_EMPRESA_LENGHT)
    valor = models.FloatField()
    data_emissao = models.DateField()

    def __str__(self):
        return str (self.cnpj_empresa) + ": " + str(self.cpf_cliente) + " - " + str(self.data_emissao)


class Cartao(models.Model):
    num_cartao = models.CharField(max_length = constant.NUM_CARTAO_LENGHT)
    cvv = models.CharField(max_length = constant.CVV_LENGHT)
    nome_cartao = models.CharField(max_length = constant.NOME_CARTAO_LENGHT)
    data_vencimento_cartao = models.DateField()
    # Credito == true //// Debito == false
    credito = models.BooleanField()
    num_parcelas = models.IntegerField()
    pedido = models.ForeignKey('Pedido', null = True, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.num_cartao)


class Boleto(models.Model):
    banco = models.CharField(max_length = constant.BANCO_LENGHT)
    num_boleto = models.CharField(max_length = constant.NUM_BOLETO_LENGHT)
    data_vencimento = models.DateField()
    nome_empresa = models.CharField(max_length = constant.NOME_EMPRESA_LENGHT)
    endereco_empresa = models.CharField (max_length = constant.ENDERECO_EMPRESA_LENGHT)
    pedido = models.ForeignKey('Pedido', null = True, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.num_boleto)
