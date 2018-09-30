# -*- coding: utf-8 -*-

from django.shortcuts import render
from datetime import *
from .model_forms import *
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import *
from .model_forms import *
from .utils import *
from django.core.exceptions import ObjectDoesNotExist
from .simulacao_banco import *

import urllib2
import json

def index(request):
    return HttpResponse("Hello, world. You're at the payment index.")


def status_boleto(request):

    try:
        '''Recupera do metodo POST a primary key do pedido'''

        pk_pagamento = json.loads(request.body)
        pk_pagamento = int(pk_pagamento['pk_pagamento'])


        '''Tenta encontrar o pedido no banco de dados. Caso o pedido nao seja encontrado, retorna uma mensagem de erro'''
        try:
            pedido = Pedido.objects.get(pk=pk_pagamento)  # Recupera o pedido desejado a partir de sua primary key
            status = Boleto.objects.get(
                pedido=pedido).status  # Recupera o status de pagamento do boleto a partir do pedido encontrado
        except ObjectDoesNotExist:
            status = 4

    except ValueError:
        status = 5

    data = {
        'status': status
    }

    return JsonResponse(data)

def CompraComCartao(request):
    if request.method == 'POST':
        # Cria o formulário e com os dados recebidos
        form_cartao = PagamentoCartaoForm(data=request.POST)
        
        # Validação das informações recebidas
        erro = False
        status = {}
        status['cpf_comprador'] = corretude_cpf(form_cartao['cpf_comprador'].value())
        status['valor_compra'] = corretude_valor(form_cartao['valor_compra'].value())
        status['cnpj_site'] = corretude_cnpj(form_cartao['cnpj_site'].value())
        status['data_emissao'] = corretude_data(form_cartao['data_emissao'].value())
        status['numero_cartao'] = corretude_numero_cartao(form_cartao['numero_cartao'].value())
        status['nome_cartao'] = corretude_nome_impresso_cartao(form_cartao['nome_cartao'].value())
        status['cvv_cartao'] = corretude_cvv(form_cartao['cvv_cartao'].value())
        status['data_vencimento_cartao'] = corretude_data_vencimento_cartao(form_cartao['data_vencimento_cartao'].value())
        status['credito'] = corretude_tipo_cartao(form_cartao['credito'].value())
        status['num_parcelas'] = corretude_num_parcelas(form_cartao['num_parcelas'].value())

        for validacao in status:
            if status[validacao] != 0:
                erro = True # caso ocorra algum erro na validação dos dados
                break

        # Realiza o pagamento junto ao banco
        pagamento = 0
        if erro == False: # Se não ocorreu nenhum erro, então tenta fazer o pagamento
            pagamento = simula_pagamento_cartao(form_cartao['numero_cartao'].value())
        else:
            pagamento = -2



        context = {
            'status_cpf_comprador': status['cpf_comprador'],
            'status_valor_compra': status['valor_compra'],
            'status_cnpj_site': status['cnpj_site'],
            'status_data_emissao': status['data_emissao'],
            'status_numero_cartao': status['numero_cartao'],
            'status_nome_cartao': status['nome_cartao'],
            'status_cvv_cartao': status['cvv_cartao'],
            'status_data_vencimento_cartao': status['data_vencimento_cartao'],
            'status_credito': status['credito'],
            'status_num_parcelas': status['num_parcelas'],
            'pagamento': pagamento,
        }
        return JsonResponse(context, json_dumps_params={'indent': 2})

    else:
        form_cartao = PagamentoCartaoForm()
        return render(request, 'pagamento_cartao.html', {'form_cartao': form_cartao})



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

    is_valid = status_cpf_comprador == 0 and status_valor_compra == 0
    is_valid = is_valid and status_cnpj_site == 0 and status_banco_gerador_boleto == 0
    is_valid = is_valid and status_data_vencimento_boleto == 0
    is_valid = is_valid and status_endereco_fisico_site == 0
    num_boleto = -1 # valor default
    if is_valid:
        num_boleto = gera_boleto(cpf_comprador, valor_compra, cnpj_site,
                                 banco_gerador_boleto, data_vencimento_boleto,
                                 endereco_fisico_site)


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
        'num_boleto' : num_boleto,
    }
    return JsonResponse(context)

def busca_pedido (request):
    pedido_form = PedidoForm()
    context = {
        'pedido_form': pedido_form
    }
    return render (request, 'servico/busca_pedido.html', context)

def busca_pedido_resultado (request):
    pedido_form = PedidoForm(data=request.POST)
    try:
        pedido = Pedido.objects.get(pk = pedido_form['pedido_id'].value())
        status_pedido = 1
    except:
        status_pedido = 0

    try:
        cartao = Cartao.objects.get(pedido = pedido)
        cartao_boleto = True
    except:
        pass

    try:
        boleto = Boleto.objects.get(pedido = pedido)
        cartao_boleto = False
    except:
        pass

    if (status_pedido == 1):
        cpf_cliente = pedido.cpf_cliente
        cnpj_empresa = pedido.cnpj_empresa
        valor = pedido.valor
        data_emissao = pedido.data_emissao
        if cartao_boleto:
            num_cartao = cartao.num_cartao
            cvv = cartao.cvv
            nome_cartao = cartao.nome_cartao
            data_vencimento_cartao = cartao.data_vencimento_cartao
            credito = cartao.credito
            num_parcelas = cartao.num_parcelas
            banco = None
            num_boleto = None
            data_vencimento = None
            nome_empresa = None
            endereco_empresa = None
            status = None
        else:
            num_cartao = None
            cvv = None
            nome_cartao = None
            data_vencimento_cartao = None
            credito = None
            num_parcelas = None
            banco = boleto.banco
            num_boleto = boleto.num_boleto
            data_vencimento = boleto.data_vencimento
            nome_empresa = boleto.nome_empresa
            endereco_empresa = boleto.endereco_empresa
            status = boleto.status
    else:
        cpf_cliente = None
        cnpj_empresa = None
        valor = None
        data_emissao = None
        cartao_boleto = None
        num_cartao = None
        cvv = None
        nome_cartao = None
        data_vencimento_cartao = None
        credito = None
        num_parcelas = None
        banco = None
        num_boleto = None
        data_vencimento = None
        nome_empresa = None
        endereco_empresa = None
        status = None

    data = {
        'status_pedido': status_pedido,
        'cpf_cliente': cpf_cliente,
        'cnpj_empresa': cnpj_empresa,
        'valor': valor,
        'data_emissao': data_emissao,
        'cartao_boleto': cartao_boleto,
        'num_cartao': num_cartao,
        'cvv': cvv,
        'nome_cartao': nome_cartao,
        'data_vencimento_cartao': data_vencimento_cartao,
        'credito': credito,
        'num_parcelas': num_parcelas,
        'banco': banco,
        'num_boleto': num_boleto,
        'data_vencimento': data_vencimento,
        'nome_empresa': nome_empresa,
        'endereco_empresa': endereco_empresa,
        'status': status
    }

    return JsonResponse(data)

def teste(request):

    url = 'http://127.0.0.1:8000/servico/status_boleto'

    status = {
        'pk_pagamento': '5'
    }

    data = json.dumps(status)

    request2 = urllib2.Request(url, data)

    try:
        # serializade_data = urllib2.urlopen(request2, data=json.dumps(data))
        serializade_data = urllib2.urlopen(request2).read()
    except Exception, e:
        print e.code
        print e.read()

    resposta = json.loads(serializade_data)

    return HttpResponse('Retorno: {}'.format(resposta['status']))