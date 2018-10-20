from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Produtos(models.Model):
    id_produto = models.CharField(max_length=100, default='-1')

class Usuario(models.Model):
    email = models.CharField(max_length=150)
    cpf = models.CharField(max_length=15)
    sessionToken = models.CharField(max_length=300)
