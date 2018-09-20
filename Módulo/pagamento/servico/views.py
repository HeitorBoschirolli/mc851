# -*- coding: utf-8 -*-

from django.shortcuts import render
from datetime import *
from .model_forms import *
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the payment index.")


def CompraComCartao(request):
    if request.method == 'POST':
        form_cartao = PagamentoCartaoForm(data=request.POST)
        context = {
            'form_cartao': form_cartao,
            'status': 1,
            'mensagem': 'Pagamento Aprovado',
            'pk_pagamento': 1,
        }
        return render(request, 'pagamento_cartao.html', context)

    else:
        form_cartao = PagamentoCartaoForm()
        return render(request, 'pagamento_cartao.html', {'form_cartao': form_cartao})


    #return render(request, 'pagamento_cartao_interface.html', context)
    # mensagem = ''

    # # Cartão
    # num_cartao = request.POST('num_cartao', '123')
    # cvv = request.POST('cvv', '123')
    # nome_cartao = request.POST('nome_cartao', 'Paulo')
    # data_vencimento_cartao_str = request.POST('data_vencimento_cartao', '11-2018')
    # credito = request.POST('credito', '1')
    # num_parcelas = int(request.POST('num_parcelas', '2'))
    # pedido = request.POST('pedido', '1')

    # # Pedido
    # cpf_cliente = request.POST('cpf_cliente', '123')
    # cnpj_empresa = request.POST('cnpj_empresa', '123')
    # valor = int(request.POST('valor', '123'))
    # data_emissao = request.POST('data_emissao', '10-12-2018')


    # ### Início Tratamento de erros ###

    # # Se cartão estiver vencido retorna erro
    # hoje = datetime.now()
    # data_vencimento_cartao = datetime.strptime('data_vencimento_cartao_str', '%m-%Y')
    # if not hoje < data_vencimento_cartao:
    #     mensagem = 'Cartão Vencido'

    # # Se for débito com parcelas retorna erro
    # if num_parcelas > 1 and credito == 0:
    #     mensagem = 'Numero de parcelas não condiz com o tipo de cartão'

    # if valor <= 0:
    #     mensagem = 'Valor incorreto'

    # ### Fim Tratamento de erros ###




