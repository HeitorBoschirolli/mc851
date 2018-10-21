from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Produtos(models.Model):
    id_produto = models.CharField(max_length=100, default='-1')

    def __str__ (self):
        return str(self.id_produto)

class Carrinho(models.Model):
    total = models.IntegerField(default=0)

class Usuario(models.Model):
    email = models.CharField(max_length=150)
    cpf = models.CharField(max_length=15)
    sessionToken = models.CharField(max_length=300)
    carrinho = models.OneToOneField(Carrinho, on_delete=models.CASCADE, null=True)

    def __str__ (self):
        return str(self.email) + " : " + str(self.cpf)

class Pedidos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, null=False)
    carrinho = models.OneToOneField(Carrinho, on_delete=models.CASCADE, null=False)

class Produtos_no_Carrinho(models.Model):
    produto = models.ForeignKey(Produtos, on_delete=models.DO_NOTHING, null=False)
    quantidade = models.IntegerField()
    carrinho = models.ForeignKey(Carrinho, on_delete=models.DO_NOTHING, null=False)
