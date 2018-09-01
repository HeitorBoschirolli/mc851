from django.http import HttpResponse
from django.shortcuts import render
from .models import *


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def get_pagamento(request, cpf):
    pedidos = Pedido.objects.filter(cpf=cpf)


    return render(request, 'pagamento/pagamento.html')