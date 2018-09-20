# -*- coding: utf-8 -*-

from django.shortcuts import render
from datetime import *
from .model_forms import *
from django.http import HttpResponse
from django.template import loader
from .models import *
from .model_forms import *
from .utils import *
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    return HttpResponse("Hello, world. You're at the payment index.")

def input(request, pk):

    primary_key = PrimaryKey()
    primary_key.pk1 = pk

    context = {
        'pk': primary_key,
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
    # # Cartao
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


def pagamento_boleto(request):
    form_cartao = PagamentoBoletoForm()
    context = {
        'form_cartao': form_cartao,
    }
    return render(request, 'servico/get_infos_boleto.html', context)

def feedback_pagamento_boleto(request):
    form_boleto = PagamentoBoletoForm(data=request.POST)

    cpf_comprador = form_boleto['cpf_comprador'].value()
    valor_compra = form_boleto['valor_compra'].value()
    cnpj_site = form_boleto['cnpj_site'].value()
    banco_gerador_boleto = form_boleto['banco_gerador_boleto'].value()
    banco_gerador_boleto = formata_banco(banco_gerador_boleto)
    data_vencimento_boleto = form_boleto['data_vencimento_boleto'].value()
    endereco_fisico_site = form_boleto['endereco_fisico_site'].value()

    status_cpf_comprador = corretude_cpf(cpf_comprador)
    status_valor_compra = corretude_valor(valor_compra)
    status_cnpj_site = corretude_cnpj(cnpj_site)
    status_banco_gerador_boleto = corretude_banco(banco_gerador_boleto)
    status_data_vencimento_boleto = corretude_data(data_vencimento_boleto)
    status_endereco_fisico_site = corretude_endereco_fisico(
                                                            endereco_fisico_site
                                                            )

    context = {
        'cpf_comprador' : cpf_comprador,
        'valor_compra' : valor_compra,
        'cnpj_site' : cnpj_site,
        'banco_gerador_boleto' : banco_gerador_boleto,
        'data_vencimento_boleto' : data_vencimento_boleto,
        'endereco_fisico_site' : endereco_fisico_site,
        'status_cpf_comprador': status_cpf_comprador,
        'status_valor_compra': status_valor_compra,
        'status_cnpj_site': status_cnpj_site,
        'status_banco_gerador_boleto': status_banco_gerador_boleto,
        'status_data_vencimento_boleto': status_data_vencimento_boleto,
        'status_endereco_fisico_site': status_endereco_fisico_site,
    }
    return render(request, 'servico/feedback_pagamento_boleto.html', context)
