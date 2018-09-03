from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Cliente(models.Model):
    nome = models.CharField(max_length=50)
    CPF = models.CharField(max_length=20)
    endereco = models.CharField(max_length=200)
    email = models.EmailField(max_length=70,blank=True)
    telefone = models.CharField(max_length=20)
    RG = models.IntegerField()

    def __str__(self):
        return self.nome
    


class Pedido(models.Model):
    valor = models.FloatField()
    infos_produto = models.TextField(max_length=200)

    def __str__(self):
        return (self.infos_produto + " | Valor: R$" + str(self.valor))


class Pagamento(models.Model):
    cliente = models.ForeignKey('Cliente', null=True, on_delete=models.CASCADE)
    pedido = models.ForeignKey('Pedido', null=True, on_delete=models.CASCADE)

    cartao = models.ForeignKey('Cartao', blank=True, null=True, on_delete=models.CASCADE)
    boleto = models.ForeignKey('Boleto', blank=True, null=True, on_delete=models.CASCADE)


class Cartao(models.Model):
    bandeira_cartao = models.CharField(max_length=30)
    num_parcelas = models.IntegerField()
    num_cartao = models.CharField(max_length=20)
    juros = models.FloatField()
    nome_cartao = models.CharField(max_length=50)
    data_vencimento_cartao = models.DateField()
    CVV = models.IntegerField()
    credito = models.BooleanField()
    debito = models.BooleanField()

    #pagamento = GenericRelation(Pagamento)

    def __str__(self):
        return self.bandeira_cartao
    

class Boleto(models.Model):
    data_vencimento = models.DateField()
    banco = models.CharField(max_length=50)
    numero_boleto = models.CharField(max_length=50, default="0")
    status = models.BooleanField()
    #pagamento = GenericRelation(Pagamento)

    def __str__(self):
        return self.numero_boleto


