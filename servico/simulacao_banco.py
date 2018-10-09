# -*- coding: utf-8 -*-

# Aprova ou nega pagamento de acordo com o número do cartão
# return 1 --> Últimos 4 digitos = "1111" --> aprova compra
# return 0 --> Caso contrário --> compra é negada

def simula_pagamento_cartao(numero_cartao):
    ultimos_4_digitos = numero_cartao[-4:]
    if ultimos_4_digitos == "1111":
        return 1 # compra aprovada
    else:
        return -1 # compra negada
