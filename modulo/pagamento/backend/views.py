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

url_clientes = "ec2-18-231-28-232.sa-east-1.compute.amazonaws.com:3002/"

#Renderiza a pagina inicial do site
def home(request):
    return render(request, 'backend/home.html')


def recuperar(request):
    return render(request, 'backend/recuperar.html')


'''---------------------------------------------------------------------------------------------------------'''
'''---------------------------------------------API DE ENDERECO---------------------------------------------'''
'''---------------------------------------------------------------------------------------------------------'''

#Renderiza a pagina que ira enviar o cep do endereco a ser pesquisado na api de enderecos
def endereco_cliente(request):

    # Recupera do forms enviado pelo html o cep
    endereco = DadosEndereco()

    # Passa o forms como contexto para ser utilizado para obtencao de dados no html
    context = {
        'endereco': endereco
    }

    return render(request=request, template_name='backend/endereco_cep.html', context=context)


#Funcao que ira requisitar a api de enderecos, os dados de uma busca de endereco por cep
def endereco_cep(request):

    #URL com o endereco da api para fazer a requisicao
    url = 'http://wsendereco.tk/api/enderecos/cep/'

    endereco = DadosEndereco(data=request.POST)

    url = url + endereco['cep'].value()

    request2 = urllib2.Request(url=url, headers={'Content-Type': 'application/json'})

    try:
        # serializade_data = urllib2.urlopen(request2, data=json.dumps(data))
        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        context = {
            'bairro': resposta['Endereco'][0]['bairro'],
            'cidade': resposta['Endereco'][0]['cidade'],
            'inicio': resposta['Endereco'][0]['inicio'],
            'logradouro': resposta['Endereco'][0]['logradouro'],
            'longitude': resposta['Endereco'][0]['longitude'],
            'cep': resposta['Endereco'][0]['cep'],
            'latitude': resposta['Endereco'][0]['latitude'],
            'estado': resposta['Endereco'][0]['estado'],
            'fim': resposta['Endereco'][0]['fim']
        }
        # return JsonResponse(resposta)
        return render(
            request=request,
            template_name="backend/confirma_endereco.html",
            context=context
        )

    except Exception as e:

        return JsonResponse({'error': e.code})


'''---------------------------------------------------------------------------------------------------------'''
'''---------------------------------------------API DE CLIENTES---------------------------------------------'''
'''---------------------------------------------------------------------------------------------------------'''


#Renderiza pagina que ira receber os dados do cliente para cadastrar na api de clientes
def dados_cliente(request):

    cliente = DadosCliente()

    # Passa o forms como contexto para ser utilizado para obtencao de dados no html
    context = {
        'cliente': cliente
    }

    return render(
        request=request,
        template_name='backend/cadastro_cliente.html',
        context=context
    )


#Cadastra um cliente no modulo de clientes
def cadastra_cliente(request):

    #Recupera do forms enviado pelo html, os dados do cliente
    form_cliente = DadosCliente(data=request.POST)

    url = 'http://ec2-18-231-28-232.sa-east-1.compute.amazonaws.com:3002/register'

    data = {
        "email": form_cliente['email'].value(),
        "senha": form_cliente['senha'].value(),
        "cpf": form_cliente['cpf'].value(),
        "nome": form_cliente['nome_cliente'].value(),
        "dataDeNascimento": form_cliente['data_nascimento'].value(),
        "telefone": form_cliente['telefone'].value(),
        "idGrupo": 5
    }

    data = json.dumps(data)

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    try:
        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        context = {
            'registerToken': resposta['registerToken']
        }

        # return JsonResponse(resposta)
        return render(request=request, template_name='backend/confirma_cadastro.html', context=context)

    except Exception as e:

        return JsonResponse({'error': e.code})


# Confirma o cadastro de um cliente
def confirma_cadastro(request):

    # Url da api de clientes para confirmar o cadastramento do usuario
    url = 'http://ec2-18-231-28-232.sa-east-1.compute.amazonaws.com:3002/confirm'

    # Obtem da request, o token de sessao
    register_token = request.POST.get('registerToken')

    # Monta o JSON com o registerToken para que a API de clientes confirme o cadastramento do usuario
    data = {
        'registerToken': register_token
    }

    data = json.dumps(data)

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    try:
        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        return render(request=request, template_name='backend/cadastro_cliente_confirmado.html')

    except Exception as e:

        return JsonResponse({'error': e})


#Renderiza a pagina de login
def login(request):

    # Instancia um forms para os dados do cliente
    cliente = DadosCliente()

    # Passa o forms como contexto para ser utilizado para obtencao de dados no html
    context = {
        'cliente': cliente,
        'sucesso': None,
    }

    return render(request=request, template_name='backend/login.html', context=context)

#Realiza o login na api de clientes
def resultado_login(request):

    #Recupera do forms enviado pelo html, os dados do cliente
    form_cliente = DadosCliente(data=request.POST)

    url ='http://ec2-18-231-28-232.sa-east-1.compute.amazonaws.com:3002/login'

    data = {
        "email": form_cliente['email'].value(),
        "senha": form_cliente['senha'].value(),
    }

    data = json.dumps(data)

    request2 = urllib2.Request(
        url=url,
        data=data,
        headers={'Content-Type': 'application/json'}
    )

    try:
        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        context = {
            'registerToken': resposta['sessionToken']
        }

        return render(request=request, template_name='backend/login_confirmado.html')

    except Exception as e:

        cliente = DadosCliente()

        context = {
            'cliente': cliente,
            'sucesso': True,
        }

        return render(request=request, template_name='backend/login.html', context=context)


'''---------------------------------------------------------------------------------------------------------'''
'''---------------------------------------------API DE PRODUTOS---------------------------------------------'''
'''---------------------------------------------------------------------------------------------------------'''

def produtos_eletrodomesticos(request, pagina):
    #produtos (request, pagina, "eletromestico")
    return render(request=request, template_name='backend/produtos.html')

def produtos_computadores(request, pagina):
    #produtos (request, pagina, "computador")
    return HttpResponse("comp" + str(pagina))

def produtos_celulares(request, pagina):
    #produtos (request, pagina, "celular")
    return HttpResponse("celulares" + str(pagina))

def produtos (request, pagina, categoria):

    url = 'ec2-18-218-218-216.us-east-2.compute.amazonaws.com:8080/api/products'

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    try:
        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        context = {
            'registerToken': resposta['registerToken']
        }

        # return JsonResponse(resposta)
        return render(request=request, template_name='backend/confirma_cadastro.html', context=context)

    except Exception as e:

        return JsonResponse({'error': e.code})
