from django.shortcuts import render
from datetime import *
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import *
from django.core.exceptions import ObjectDoesNotExist
import urllib2
import json
import base64
from model_forms import *

# Create your views here.

def teste(request):

    #Instancia um forms para os dados do cliente
    cliente = DadosCliente()

    #Passa o forms como contexto para ser utilizado para obtencao de dados no html
    context = {
        'cliente': cliente
    }

    return render(request=request, template_name='backend/cadastro_cliente.html', context=context)



#Cadastra um cliente no modulo de clientes
def cadastra_cliente(request):

    #Recupera do forms enviado pelo html, os dados do cliente
    form_cliente = DadosCliente(data=request.POST)

    url = 'http://ec2-18-231-28-232.sa-east-1.compute.amazonaws.com:3002/register'

    data = {
        "email": form_cliente['nome_cliente'].value(),
        "senha": form_cliente['senha'].value(),
        "cpf": form_cliente['cpf'].value(),
        "nome": form_cliente['nome_cliente'].value(),
        "dataDeNascimento": form_cliente['data_nascimento'].value(),
        "telefone": form_cliente['telefone'].value(),
        "idGrupo": form_cliente['id_grupo'].value()
    }

    data = json.dumps(data)

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    import pdb
    pdb.set_trace()

    try:
        # serializade_data = urllib2.urlopen(request2, data=json.dumps(data))
        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        return JsonResponse(resposta)

    except Exception as e:

        return JsonResponse({'error': e.code})




def pagamentos(request):

    url = 'http://pagamento.4pmv2bgufu.sa-east-1.elasticbeanstalk.com/servico/status_boleto'

    # data = json.dumps(status)
    # data = json.loads(request.body)

    data = {
        "pk_pagamento": '2'
    }

    data = json.dumps(data)

    # base64string = base64.b64encode('%s:%s' % ('test', 'senhatest'))

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})
    # request2.add_header("Authorization", "Basic %s" % base64string)

    # request2.add_header('Content-Type': 'application/json')

    # import pdb
    # pdb.set_trace()

    try:
        # serializade_data = urllib2.urlopen(request2, data=json.dumps(data))
        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        return JsonResponse(resposta)

    except urllib2.URLError as e:
        print(e)
        return JsonResponse({'error': e.code})

