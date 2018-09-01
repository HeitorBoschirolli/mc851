from django.db import models


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
    cartao = models.ForeignKey('Cartao', null=True, on_delete=models.CASCADE)
    boleto = models.ForeignKey('Boleto', null=True, on_delete=models.CASCADE)
    pedido = models.ForeignKey('Cliente', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.valor


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

    def __str__(self):
        return self.bandeira_cartao


class Boleto(models.Model):
    data_vencimento = models.DateField()
    banco = models.CharField(max_length=50)



