from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Acesso_API (models.Model):
    API = models.CharField(max_length=100)
    data_acesso = models.DateField ()
    descricao = models.CharField (max_length=500, null=True)

    def __str__ (self):
        return str(self.API) + ": " + str(self.descricao) + " - " + str(self.data_acesso)


class Produtos(models.Model):
    id_produto = models.CharField(max_length=100, default='-1')

    def __str__ (self):
        return str(self.id_produto)

class Carrinho(models.Model):
    total_carrinho = models.FloatField(default=0)
    total_frete = models.FloatField(default=0)
    cep = models.CharField(max_length=100, null=True)
    numero_residencia = models.CharField(max_length=100, null=True)
    complemento = models.CharField(max_length=100, null=True)
    id_pagamento = models.IntegerField(default=-1)
    id_logistica = models.CharField(max_length=500, null=True)

    def __str__ (self):
        return "carrinho: " + str(self.pk)

class Usuario(models.Model):
    email = models.CharField(max_length=150)
    cpf = models.CharField(max_length=15)
    sessionToken = models.CharField(max_length=300)
    admin = models.BooleanField(default=False)
    carrinho = models.OneToOneField(Carrinho, on_delete=models.CASCADE, null=True)

    def __str__ (self):
        return str(self.email) + " : " + str(self.cpf)

class Pedidos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, null=False)
    carrinho = models.OneToOneField(Carrinho, on_delete=models.CASCADE, null=False)

    def __str__ (self):
        return "Pedido do usuario: " + str(self.usuario) + " com carrinho: " + str(self.carrinho)

class Produtos_no_Carrinho(models.Model):
    produto = models.ForeignKey(Produtos, on_delete=models.DO_NOTHING, null=False)
    quantidade = models.IntegerField(default=1)
    valor_unitario = models.FloatField(default=-1)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.DO_NOTHING, null=False)

    def __str__ (self):
        return "Produto: " + str(self.produto) + " no carrinho: " + str(self.carrinho)
