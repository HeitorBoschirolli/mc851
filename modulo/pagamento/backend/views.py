# -*- coding: utf-8 -*-

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
    _ = get_produtos(request)

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
        'endereco': endereco,
        'cep_failed': False
    }

    return render(
        request=request,
        template_name='backend/endereco_cep.html',
        context=context
    )


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
            'fim': resposta['Endereco'][0]['fim'],
        }
        # return JsonResponse(resposta)
        return render(
            request=request,
            template_name="backend/confirma_endereco.html",
            context=context
        )

    except:
        endereco = DadosEndereco()
        context = {
            'endereco': endereco,
            'cep_failed': True
        }
        return render(
            request,
            template_name="backend/endereco_cep.html",
            context=context
        )


'''---------------------------------------------------------------------------------------------------------'''
'''---------------------------------------------API DE CLIENTES---------------------------------------------'''
'''---------------------------------------------------------------------------------------------------------'''


#Renderiza pagina que ira receber os dados do cliente para cadastrar na api de clientes
def dados_cliente(request):

    cliente = DadosCliente()

    # Passa o forms como contexto para ser utilizado para obtencao de dados no html
    context = {
        'cliente': cliente,
        'error': False
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

    filtro = Usuario.objects.filter(email=data['email'])
    if (filtro.count() > 0):
        cliente = DadosCliente()
        context = {
            'cliente': cliente,
            'error': False,
            'cadastro': True,
        }

        return render(
            request=request,
            template_name='backend/cadastro_cliente.html',
            context=context
        )

    data = json.dumps(data)

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    try:

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        context = {
            'registerToken': resposta['registerToken'],
        }

        usuario = Usuario()
        usuario.email = str(form_cliente['email'].value())
        usuario.cpf = str(form_cliente['cpf'].value())
        usuario.sessionToken = ''
        carrinho = Carrinho(total = 0)
        carrinho.save()
        usuario.carrinho = carrinho
        usuario.save()

        # return render(
        #     request=request,
        #     template_name='backend/confirma_cadastro.html',
        #     context=context
        # )
        return confirma_cadastro(request)

    except:
        cliente = DadosCliente()
        context = {
            'cliente': cliente,
            'error': True,
            'cadastro': False,
        }

        return render(
            request=request,
            template_name='backend/cadastro_cliente.html',
            context=context
        )
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

    request2 = urllib2.Request(
        url=url,
        data=data,
        headers={'Content-Type': 'application/json'}
    )

    try:
        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        return render(
            request=request,
            template_name='backend/cadastro_cliente_confirmado.html'
        )

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

    return render(
        request=request,
        template_name='backend/login.html',
        context=context
    )

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

        # Trocar para nome do cliente
        request.session['usuario'] = form_cliente['email'].value()

        context = {
            'sessionToken': resposta['sessionToken']
        }

        usuario = Usuario.objects.get(email=str(form_cliente['email'].value()))
        usuario.sessionToken = resposta['sessionToken']
        usuario.save()

        return render(
            request=request,
            template_name='backend/login_confirmado.html'
        )

    except Exception as e:

        cliente = DadosCliente()

        context = {
            'cliente': cliente,
            'sucesso': True,
        }

        return render(
            request=request,
            template_name='backend/login.html',
            context=context
        )

def logout(request):
    request.session['usuario'] = ''

    return render(request=request, template_name='backend/home.html')


def minha_conta(request):

    context = {
        }

    return render(
        request=request,
        template_name='backend/minha_conta.html',
        context=context
    )

'''---------------------------------------------------------------------------------------------------------'''
'''---------------------------------------------API DE PRODUTOS---------------------------------------------'''
'''---------------------------------------------------------------------------------------------------------'''


#Funcao que realiza um request para a api de produtos para pegar a lista de produtos
def get_produtos(request, pagina='0'):
    url = 'http://ec2-18-218-218-216.us-east-2.compute.amazonaws.com:8080/api/products?page=' + pagina + '&itemsPerPage=1000'

    request2 = urllib2.Request(url=url)

    #Adiciona ao request o login de autorizacao
    basic_auth = base64.b64encode('%s:%s' % ('pagamento', 'LjKDBeqw'))
    request2.add_header("Authorization", "Basic %s" % basic_auth)

    try:

        # Realiza o request e obtem os dados retornados
        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        #Lista com os produtos retornados
        produtos = resposta['content']

        # Cria as categorias existentes dos produtos retornados e salva na session
        categorias_dict = {}
        categorias = []

        for produto in produtos:
            # Cria uma lista com os tipos de categorias existentes
            categoria_produto = produto['category']
            if categoria_produto not in categorias_dict:
                categorias_dict[categoria_produto] = 1
                categorias.append(categoria_produto)

        request.session['categorias'] = categorias

        #Adiciona os ids dos produtos no banco de dados
        # for i in range(0, len(produtos)):

        #     if(Produtos.objects.filter(id_produto=resposta['content'][i]['id']) == False):

        #         p = Produtos()
        #         p.id_produto = resposta['content'][i]['id']
        #         p.save()

        #JSON com a lista de produtos que sera
        # context = {
        #     #'produtos': produtos_filtrados,
        #     'produtos': produtos,
        # }

        # return JsonResponse(context)
        #return render(request=request, template_name='backend/produtos.html', context=context)
        return produtos

    except Exception as e:

        return JsonResponse({'error': e})

def produtos(request, categoria, pagina):

    produtos = get_produtos(request, pagina)

    #Lista com os produtos retornados
    produtos_filtrados = []

    for produto in produtos:
        # Seleciona apenas os produtos da categoria recebida
        if produto['category'] == categoria:
            produtos_filtrados.append(produto)

    context = {
            'produtos': produtos_filtrados,
        }


    return render(
        request=request,
        template_name='backend/produtos.html',
        context=context
    )

#Funcao que renderiza a pagina para o admin que ira atualizar os dados de um produto
def render_att_produtos(request):

    # Instancia um forms para os dados do Produto
    produto = DadosProduto()

    # Passa o forms como contexto para ser utilizado para obtencao de dados no html
    context = {
        'produto': produto,
    }

    return render(
        request=request,
        template_name='backend/admin_dados_produto.html',
        context=context
    )


#Funcao que atualiza as informacoes de um produto
def att_produto(request):

    #Recebe o id do produto por post
    form_Produto = DadosProduto(data=request.POST)
    id_produto = form_Produto['id_produto'].value()

    #PROCURA O PRODUTO NA API DE PRODUTOS, PARA QUE SEUS DADOS SEJAM ATUALIZADOS

    #Url da requisicao
    url = 'http://ec2-18-218-218-216.us-east-2.compute.amazonaws.com:8080/api/products/' + id_produto

    request2 = urllib2.Request(url=url)

    # Adiciona ao request o login de autorizacao
    basic_auth = base64.b64encode('%s:%s' % ('pagamento', 'LjKDBeqw'))
    request2.add_header("Authorization", "Basic %s" % basic_auth)

    #Realiza uma requisicao ao modulo de produtos para obter os dados do produto
    try:
        serializade_data = urllib2.urlopen(request2).read()
        dados_produto = json.loads(serializade_data)

    except Exception as e:

        return JsonResponse({'error': e})

    #Atualiza os dados que o admin quer que sejam atualizados
    for key in form_Produto.fields:

        if(form_Produto[key].data):
            dados_produto[key] = form_Produto[key].data


    #ATUALIZA OS DADOS DO PRODUTO

    # Url da requisicao
    url = 'http://ec2-18-218-218-216.us-east-2.compute.amazonaws.com:8080/api/products/' + id_produto

    data = json.dumps(dados_produto)
    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})
    request2.get_method = lambda: 'PATCH'

    basic_auth = base64.b64encode('%s:%s' % ('pagamento', 'LjKDBeqw'))
    request2.add_header("Authorization", "Basic %s" % basic_auth)

    #Envia a requsicao ao modulo
    try:
        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        return JsonResponse(resposta)

    except Exception as e:

        return JsonResponse({'error': e})

'''---------------------------------------------------------------------------------------------------------'''
'''--------------------------------------------API DE PAGAMENTO---------------------------------------------'''
'''---------------------------------------------------------------------------------------------------------'''


#Realiza um pagamento por cartão
def pagamento_cartao(request):

    #Recupera os dados do pagamento para enviar para a api de pagamento
    # forms_pagamento = Pagamento(data=request.POST)

    #URL para api de pagamento
    url = 'http://pagamento.4pmv2bgufu.sa-east-1.elasticbeanstalk.com/servico/pagamento_cartao'

    # Variaveis de teste
    data = {
        "cpf_comprador": "12356712345",
        "valor_compra": "10.20",
        "cnpj_site": "12345678992735",
        "data_emissao_pedido": "2/10/2018",
        "numero_cartao": "1234123412341111",
        "nome_cartao": "SINDAO",
        "cvv_cartao": "123",
        "data_vencimento_cartao": "2/10/2025",
        "credito": "1",
        "num_parcelas": "2"
    }

    data = json.dumps(data)

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    try:

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)


        return JsonResponse(resposta)

    except Exception as e:
        return JsonResponse({'error': e.code})


#Realiza um pagamento por boleto
def pagamento_boleto(request):

    #Recupera os dados do pagamento para enviar para a api de pagamento
    # forms_pagamento = Pagamento(data=request.POST)

    #URL para api de pagamento
    url = 'http://pagamento.4pmv2bgufu.sa-east-1.elasticbeanstalk.com/servico/pagamento_boleto'

    # Variaveis de teste
    data = {
        "cpf_comprador": "12356712345",
        "valor_compra":"10.20",
        "cnpj_site":"12345678992735",
        "banco_gerador_boleto":"Itau",
        "data_vencimento_boleto":"04/10/2018",
        "endereco_fisico_site":"Rua Sindo",
        "data_emissao_pedido": "25/06/2018"
    }

    data = json.dumps(data)

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    try:

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)


        return JsonResponse(resposta)

    except Exception as e:

        return JsonResponse({'error': e.code})

#Consulta um pagamento
def consulta_pagamento(request):

    #Recupera os dados do pagamento para enviar para a api de pagamento
    # forms_pagamento = Pagamento(data=request.POST)

    #URL para api de pagamento
    url = 'http://pagamento.4pmv2bgufu.sa-east-1.elasticbeanstalk.com/servico/busca_pedido'

    # Variaveis de teste
    data = {
        "pk_pagamento": "1"
    }

    data = json.dumps(data)

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    try:

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)


        return JsonResponse(resposta)

    except Exception as e:

        return JsonResponse({'error': e.code})

def pagamento(request):
    return render(request=request, template_name='backend/pagamento.html')


# Acessa a pagina do meu carrinho, mostrando um resumo de todos produtos contidos nele
def meu_carrinho(request):
    usuario = Usuario.objects.get(email=request.session['usuario'])

    produtos = []

    url = 'http://ec2-18-218-218-216.us-east-2.compute.amazonaws.com:8080/api/products/'

    for produto_no_carrinho in usuario.carrinho.produtos_no_carrinho_set.all():
        url_pedido_atual = url + str(produto_no_carrinho.produto.id_produto)

        request2 = urllib2.Request(url=url_pedido_atual)

        # Adiciona ao request o login de autorizacao
        basic_auth = base64.b64encode('%s:%s' % ('pagamento', 'LjKDBeqw'))
        request2.add_header("Authorization", "Basic %s" % basic_auth)

        #Realiza uma requisicao ao modulo de produtos para obter os dados do produto
        try:
            serializade_data = urllib2.urlopen(request2).read()
            dados_produto = json.loads(serializade_data)
            produtos.append(dados_produto)
        except Exception as e:
            return JsonResponse({'error': e.code})

    context = {
        'produtos': produtos
    }

    return render (
        request=request,
        template_name='backend/meu_carrinho.html',
        context=context
    )


# Recebe um produto do front end (id) e o adciona ao carrinho do usuario da sessao atual
def adciona_carrinho(request):

    id_produto = request.POST.get("id_produto")

    usuario = Usuario.objects.get(email=request.session['usuario'])

    if (Produtos.objects.get(id_produto=id_produto)):
        produto_no_carrinho = Produtos_no_Carrinho()
        produto_no_carrinho.produto = Produtos.objects.get(id_produto=id_produto)
        produto_no_carrinho.quantidade = 1
        produto_no_carrinho.carrinho = usuario.carrinho
        produto_no_carrinho.save()
    else:
        produto = Produtos()
        produto.id_pedido = id_produto
        produto.save()
        produto_no_carrinho = Produtos_no_Carrinho()
        produto_no_carrinho.produto = produto
        produto_no_carrinho.quantidade = 1
        produto_no_carrinho.carrinho = usuario.carrinho
        produto_no_carrinho.save()

    context = {}

    return render(
        request=request,
        template_name='backend/home.html',
        context=context
    )

# Remove um produto do carrinho
def remove_carrinho(request):

    usuario = Usuario.objects.get(email=request.session['usuario'])
    id_produto = request.POST.get("id_produto")

    for produto_no_carrinho in usuario.carrinho.produdos_no_carrinho_set.all():
        if (produto_no_carrinho.produto.id_produto == id_produto):
            produto_no_carrinho.delete()

    return meu_carrinho(request)



def teste_carrinho(request):

    return render(request=request, template_name='backend/meu_carrinho.html')


'''---------------------------------------------------------------------------------------------------------'''
'''--------------------------------------------API DE LOGISTICA---------------------------------------------'''
'''---------------------------------------------------------------------------------------------------------'''

#Funcao que pega o valor de frete da api de logistica
def get_valor_frete(request):

    #URL para acesso da api (VAI PRECISAR SER ALTERADA DEPOIS)
    url = 'https://frete-grupo06.herokuapp.com/search'

    #Pega o cep do cliente passado por um post, por meio do id 'cep'
    cep = request.POST.get('cep')

    data = {
        'codigo': cep
    }

    data = json.dumps(data)

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    try:
        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        return JsonResponse(resposta)

    except Exception as e:

        return JsonResponse({'error': e})


'''---------------------------------------------------------------------------------------------------------'''
'''---------------------------------------------API DE CRÉDITO----------------------------------------------'''
'''---------------------------------------------------------------------------------------------------------'''

#Funcao que pega o score de um cliente na api de credito
def get_score(request):

    #Pega o cpf do cliente passado no momento do pagamento
    #cpf = request.POST.get('cpf')
<<<<<<< HEAD
    cpf=str("20314520369")
=======
    cpf = '20314520369'
>>>>>>> 25f57bb432d75d2c5a021e205982486b063aefa6
    # URL para acesso da api de credito
    url = 'http://ec2-54-233-234-42.sa-east-1.compute.amazonaws.com:3000/api/v1/score/' + cpf

    request2 = urllib2.Request(url=url)

    try:
        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        return JsonResponse(resposta)

    except Exception as e:

        return JsonResponse({'error': e})
