from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .model_forms import *


def index(request):
    return HttpResponse("Hello, world. You're at the payment index.")

def busca_pedido (request):
    pedido_form = PedidoForm();
    context = {
        'pedido_form': pedido_form
    }
    return render (request, 'servico/busca_pedido.html', context)

def busca_pedido_resultado (request):
    pedido_form = PedidoForm(data=request.POST)
    try:
        pedido = Pedido.objects.get(pk = pedido_form['pedido_id'].value())        
    except:
        pedido = None

    try:
        cartao = Cartao.objects.get(pedido = pedido)
    except:
        cartao = None

    try:
        boleto = Boleto.objects.get(pedido = pedido)
    except:
        boleto = None

    context = {
        'pedido': pedido,
        'cartao': cartao,
        'boleto': boleto
    }
    return render (request, "servico/busca_pedido_resultado.html", context)
