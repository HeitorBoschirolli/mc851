import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Cliente(models.Model):
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    endereco = models.CharField(max_length=50)
    email = models.CharField(max_length=20)
    telefone = models.CharField(max_length=11)
    rg = models.CharField(max_length=9)

class Cartao(models.Model):
    valor = models.FloatField(default=0.0)
    numero_parcelas = models.IntegerField(default=0)
    juros = models.FloatField(default=0.0)
    nome_do_cartao = models.CharField(max_length=50)
    vencimento_do_cartao = models.CharField(max_length=5)
    cvv = models.IntegerField(default=0)
    credito_ou_debito = models.BooleanField(default=True) #True: credito / False: debito

class Boleto(models.Model):
    data_vencimento = models.CharField(max_length=10)
    banco_responsavel = models.CharField(max_length=20)

class Pedido(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    valor = models.FloatField(default=0.0)
    status_pagamento = models.BooleanField(default=False) #True: pago / False: pagamento nao realizado ainda
    cartao = models.ForeignKey(Cartao, null=True, on_delete=models.CASCADE, blank=True)
    boleto = models.ForeignKey(Boleto, null=True, on_delete=models.CASCADE, blank=True)
    cliente = models.ForeignKey(Cliente, null=True, on_delete=models.CASCADE, blank=False)

    def __int__(self):
        return self.id

    def __float__(self):
        return self.valor

    def __bool__(self):
        return self.status_pagamento



