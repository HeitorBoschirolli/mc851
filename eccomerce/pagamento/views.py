from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .model_forms import *
import random


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def get_pagamento(request, pk_cliente, pk_pedido):
    # try:
    #     pagamento = Pagamento.objects.get(pk=pk_pagamento)
    #     context={
    #         'pagamento':pagamento
    #     }
    # except:
    #     pass
    
    pagamento = Pagamento(
        cliente=Cliente.objects.get(pk=pk_cliente), 
        pedido=Pedido.objects.get(pk=pk_pedido)
        )

    pagamento.save()

    form_cartao = PagamentoForm()

    context={
        'form_cartao': form_cartao,
        'pagamento': pagamento,
        }


    return render(request, 'pagamento.html', context)


def resposta_pagamento(request):
    resultado_pagamento = random.choice([True, False])
    
    form_cartao = PagamentoForm(data=request.POST)
    
    pk_pagamento = request.POST.get('pk_pagamento', 0)
    tipo_pagamento = request.POST.get('tipo_pagamento', 0)
    
    if pk_pagamento:
        pagamento = Pagamento.objects.get(pk=pk_pagamento)
        if tipo_pagamento == '1':
            cartao = Cartao(
                nome_cartao = form_cartao['nome_cartao'], 
                num_cartao=form_cartao['numero_cartao'], 
                CVV=form_cartao['CVV'],
            )
            pagamento.cartao = cartao
            context = {
                'pagamento': pagamento
                }
            if resultado_pagamento == True:
                return render(request, 'sucesso.html', context)
            else:
                return render(request, 'falha.html', context)

            
def sucesso(request, context):
    return render(request, 'sucesso.html', context)
def falha(request, context):
    return render(request, 'falha.html', context)

        

    
