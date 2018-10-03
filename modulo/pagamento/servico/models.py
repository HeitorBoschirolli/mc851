from django.db import models
import datetime
from django.utils import timezone
from . import constant

class Pedido(models.Model):
    cpf_cliente = models.CharField (max_length = constant.CPF_CLIENTE_LENGTH)
    cnpj_empresa = models.CharField (max_length = constant.CNPJ_EMPRESA_LENGTH)
    valor = models.FloatField ()
    data_emissao_pedido = models.DateField ()

    def __str__(self):
        return str (self.cnpj_empresa) + ": " + str(self.cpf_cliente) + " - " + str(self.data_emissao_pedido)


class Cartao(models.Model):
    num_cartao = models.CharField (max_length = constant.NUM_CARTAO_LENGTH)
    cvv = models.CharField (max_length = constant.CVV_LENGTH)
    nome_cartao = models.CharField (max_length = constant.NOME_CARTAO_LENGTH)
    data_vencimento_cartao = models.DateField ()
    # Credito == true //// Debito == false
    credito = models.BooleanField ()
    num_parcelas = models.IntegerField ()
    pedido = models.ForeignKey ('Pedido', null = True, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.num_cartao)


class Boleto(models.Model):
    banco = models.CharField (max_length = constant.BANCO_LENGTH)
    num_boleto = models.CharField (max_length = constant.NUM_BOLETO_LENGTH)
    data_vencimento_boleto = models.DateField ()
    nome_empresa = models.CharField (max_length = constant.NOME_EMPRESA_LENGTH)
    endereco_empresa = models.CharField (max_length = constant.ENDERECO_EMPRESA_LENGTH)
    status_boleto = models.IntegerField ()
    pedido = models.ForeignKey ('Pedido', null = True, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.num_boleto)

class Banco (models.Model):
    nome = models.CharField (max_length = constant.BANCO_LENGTH)

    def __str__(self):
        return str(self.nome)
