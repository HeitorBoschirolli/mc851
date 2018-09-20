# encoding: utf-8
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from servico.models import *
from model_form import *


def index(request):
    return HttpResponse("Hello, world. You're at the payment index.")

def input(request, pk):

    aux = Aux(pk1=pk)

    context = {
        'pk': aux,
    }
    return render(request, 'input.html', context)

def status_boleto(request):

    '''Recupera do metodo POST a primary key do pedido'''
    pk_pagamento = int(request.POST.get('pk_pagamento', 0))

    '''Tenta encontrar o pedido no banco de dados. Caso o pedido nao seja encontrado, retorna uma mensagem de erro'''
    try:
        pedido = Pedido.objects.get(pk=pk_pagamento)                #Recupera o pedido desejado a partir de sua primary key
        status = Boleto.objects.get(pedido=pedido).status #Recupera o status de pagamento do boleto a partir do pedido encontrado
    except ObjectDoesNotExist:
        return HttpResponse("Pedido não encontrado")

    '''Emite resposta para teste'''
    if(status == 1):
        resposta = 'Pago'
    elif(status == 2):
        resposta = 'Aguardando Pagamento'
    elif(status == 3):
        resposta = 'Boleto Vencido'
    else:
        resposta = 'Valor desconhecido'

    return HttpResponse("Status do Pagamento: {}".format(resposta))