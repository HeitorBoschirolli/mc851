# -*- coding: utf-8 -*-

# Aprova ou nega pagamento de acordo com o número do cartão
# return 1 --> Últimos 4 digitos = "1111" --> aprova compra
# return 0 --> Caso contrário --> compra é negada

import models
from django.http import HttpResponse

def simula_pagamento_cartao(numero_cartao):
    ultimos_4_digitos = numero_cartao[-4:]
    if ultimos_4_digitos == "1111":
        return 1 # compra aprovada
    else:
        return -1 # compra negada


def simula_pagamento_boleto(request, numero_boleto, status):
    try:
        boleto = models.Boleto.objects.filter(num_boleto=numero_boleto).first()
        boleto.status_boleto = status
        boleto.save()
        mensagem = "Boleto " + numero_boleto +  " atualizado"

        return HttpResponse(mensagem)
    except:
        return HttpResponse("Número de boleto e/ou status errado")
