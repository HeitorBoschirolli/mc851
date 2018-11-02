# -*- coding: utf-8 -*-

from django.shortcuts import render
from datetime import *
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import *
from django.core.exceptions import ObjectDoesNotExist
import urllib2
import json
import base64
from model_forms import *
import random
import ast
from pdb import set_trace

url_clientes = "ec2-18-231-28-232.sa-east-1.compute.amazonaws.com:3002/"

#Renderiza a pagina inicial do site
def home(request):
    #Pega todos os produtos da lista de produtos
    save_all_products = get_produtos(request)
    all_products = save_all_products
    new_produtos = []
    for produto in all_products:
        if produto['onSale']:
            new_produtos.append(produto)
    all_products = new_produtos

    #Armazena as listas de produtos que serao mostrados na home
    produtos = []

    #Seleciona tres produtos que nao sejam repetidos
    if len(all_products) >= 3:
        #Pega o tamanho da lista de produtos
        tam = len(all_products)
        index = random.sample(range(0, tam), 3)
        produtos.append(all_products[index[0]])
        produtos.append(all_products[index[1]])
        produtos.append(all_products[index[2]])
    elif len(all_products) == 2:
        produtos = all_products
        produtos.append(all_products[0])
    elif len(all_products) == 1:
        produtos = all_products
        produtos.append(all_products[0])
        produtos.append(all_products[0])
    else:
        #Pega o tamanho da lista de produtos
        tam = len(save_all_products)
        index = random.sample(range(1, tam), 3)
        produtos.append(save_all_products[index[0]])
        produtos.append(save_all_products[index[1]])
        produtos.append(save_all_products[index[2]])


    context = {
        'produtos': produtos
    }

    return render(request, 'backend/home.html', context=context)


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

        acesso_api = Acesso_API()
        acesso_api.API = "endereco"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Buscando Endereco Dado CEP"
        acesso_api.save()

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

    #Informacoes do cliente
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    cpf = request.POST.get('cpf')
    nome = request.POST.get('nome')
    dataDeNascimento = request.POST.get('data_nascimento')
    telefone = request.POST.get('telefone')
    cep = request.POST.get('cep')
    complemento = request.POST.get('complemento')
    num_casa = request.POST.get('num_casa')

    data = {
        "email": email,
        "senha": senha,
        "cpf": cpf,
        "nome": nome,
        "dataDeNascimento": dataDeNascimento,
        "telefone": telefone,
        "idGrupo": 5
    }

    #Verifica se o email ja esta cadastrado no banco do site
    filtro = Usuario.objects.filter(email=data['email'])
    if (filtro.count() > 0):
        cliente = DadosCliente()
        context = {
            'cliente': cliente,
            'error': False,
            'cadastro': True,
        }

        return render(request=request,template_name='backend/cadastro_cliente.html',context=context
        )

    data = json.dumps(data)

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    try:

        acesso_api = Acesso_API()
        acesso_api.API = "clientes"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Cadastro de Cliente"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        #Cadastra o cliente no banco de dados do site
        usuario = Usuario()
        usuario.email = str(form_cliente['email'].value())
        usuario.cpf = str(form_cliente['cpf'].value())
        usuario.sessionToken = ''
        carrinho = Carrinho(total_carrinho = 0)
        carrinho.save()
        usuario.carrinho = carrinho
        usuario.save()

        #Confirma cadastro do cliente

        # Url da api de clientes para confirmar o cadastramento do usuario
        url = 'http://ec2-18-231-28-232.sa-east-1.compute.amazonaws.com:3002/confirm'

        # Monta o JSON com o registerToken para que a API de clientes confirme o cadastramento do usuario
        data = { 'registerToken': resposta['registerToken'] }
        data = json.dumps(data)

        request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

        try:

            acesso_api = Acesso_API()
            acesso_api.API = "clientes"
            acesso_api.data_acesso = timezone.now()
            acesso_api.descricao = "Confirmando Cadastro"
            acesso_api.save()

            serializade_data = urllib2.urlopen(request2).read()
            resposta = json.loads(serializade_data)

            #Realiza o login do cliente para cadastrar o endereco

            url = 'http://ec2-18-231-28-232.sa-east-1.compute.amazonaws.com:3002/login'

            data = {"email": email, "senha": senha}

            data = json.dumps(data)

            request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

            acesso_api = Acesso_API()
            acesso_api.API = "clientes"
            acesso_api.data_acesso = timezone.now()
            acesso_api.descricao = "Realizando Login"
            acesso_api.save()

            serializade_data = urllib2.urlopen(request2).read()
            resposta = json.loads(serializade_data)
            tokenSessao = resposta['sessionToken']

            #Pega o endereco na API de enderecos

            # URL com o endereco da api para fazer a requisicao
            url = 'http://wsendereco.tk/api/enderecos/cep/' + str(cep)

            request2 = urllib2.Request(url=url, headers={'Content-Type': 'application/json'})

            try:
                acesso_api = Acesso_API()
                acesso_api.API = "endereco"
                acesso_api.data_acesso = timezone.now()
                acesso_api.descricao = "Buscando Endereco Dado CEP"
                acesso_api.save()

                serializade_data = urllib2.urlopen(request2).read()
                resposta = json.loads(serializade_data)

                #Cadastra o endereco na api de clientes
                url = 'http://ec2-18-231-28-232.sa-east-1.compute.amazonaws.com:3002/addresses/'
                url = url + str(cpf) + '/add'

                data = {
                    'tokenSessao': tokenSessao,
                    'bairro': resposta['Endereco'][0]['bairro'],
                    'cidade': resposta['Endereco'][0]['cidade'],
                    'rua': resposta['Endereco'][0]['logradouro'],
                    'cep': resposta['Endereco'][0]['cep'],
                    'estado': resposta['Endereco'][0]['estado'],
                    'numeroCasa': num_casa,
                    'complemento': complemento
                }

                data = json.dumps(data)

                request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

                try:

                    acesso_api = Acesso_API()
                    acesso_api.API = "clientes"
                    acesso_api.data_acesso = timezone.now()
                    acesso_api.descricao = "Cadastrando Endereco do Usuario"
                    acesso_api.save()

                    serializade_data = urllib2.urlopen(request2).read()
                    resposta = json.loads(serializade_data)

                    return render(request=request, template_name='backend/cadastro_cliente_confirmado.html')

                except Exception as e:
                    return JsonResponse({'error': e})


            except:
                endereco = DadosEndereco()
                context = {
                    'endereco': endereco,
                    'cep_failed': True
                }
                return render(request,template_name="backend/endereco_cep.html",context=context)

        except Exception as e:

            return JsonResponse({'error': e})


    except:
        cliente = DadosCliente()
        context = {
            'cliente': cliente,
            'error': True,
            'cadastro': False,
        }

        return render(request=request,template_name='backend/cadastro_cliente.html',context=context)

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

        acesso_api = Acesso_API()
        acesso_api.API = "clientes"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Confirmando Cadastro"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        # return render(
        #     request=request,
        #     template_name='backend/cadastro_cliente_confirmado.html'
        # )

        return endereco_cliente(request)

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

        acesso_api = Acesso_API()
        acesso_api.API = "clientes"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Realizando Login"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        # Trocar para nome do cliente
        request.session['usuario'] = form_cliente['email'].value()

        context = {
            'sessionToken': resposta['sessionToken']
        }

        usuario = Usuario.objects.get(email=str(form_cliente['email'].value()))
        usuario.sessionToken = resposta['sessionToken']
        if usuario.admin:
            request.session['admin'] = True
        else:
            request.session['admin'] = False
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
    request.session['admin'] = False

    return home(request)


def minha_conta(request):

    try:
        usuario = Usuario.objects.get(email=request.session['usuario'])
    except:
        return dados_cliente(request)

    url = 'http://ec2-18-231-28-232.sa-east-1.compute.amazonaws.com:3002/users/'
    url = url + str(usuario.cpf)


    data = {
        "tokenSessao": str(usuario.sessionToken)
    }

    data = json.dumps(data)

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    try:

        acesso_api = Acesso_API()
        acesso_api.API = "clientes"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Recupera Dados do Usuario"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        resposta_dados = json.loads(serializade_data)
    except Exception as e:
        return JsonResponse({'error': e})

    url = 'http://ec2-18-231-28-232.sa-east-1.compute.amazonaws.com:3002/users/'
    url = url + str(usuario.cpf) + "/addresses"

    request2 = urllib2.Request(url=url, headers={'Content-Type': 'application/json'})

    try:

        acesso_api = Acesso_API()
        acesso_api.API = "clientes"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Recupera Enderecos do Usuario"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        resposta_enderecos = json.loads(serializade_data)
    except Exception as e:
        return JsonResponse({'error': e})

    # date = datetime.strptime(resposta['dataDeNascimento'], '%Y-%m-%d')

    lista_pedidos = meus_pedidos(request)
    
    form_cliente = DadosCliente()
    
    context = {
        "email": resposta_dados['email'],
        "nome": resposta_dados['nome'],
        "dataDeNascimento": resposta_dados['dataDeNascimento'],
        "telefone": resposta_dados['telefone'],
        "enderecos": resposta_enderecos,
        "lista_pedidos": lista_pedidos,
        "form_cliente": form_cliente,
        "lista_pedidios": lista_pedidos
    }

    return render(
        request=request,
        template_name='backend/minha_conta.html',
        context=context
    )

def alterar_dados_cadastrais(request):
    form_cliente = DadosCliente()

    context = {
        'cliente': form_cliente
    }

    return render (request=request, context=context, template_name="backend/alterar_dados_cadastrais.html")

def altera_dados (request):

    try:
        usuario = Usuario.objects.get(email=request.session['usuario'])
    except:
        return dados_cliente(request)

    url = 'http://ec2-18-231-28-232.sa-east-1.compute.amazonaws.com:3002/users/'
    url = url + str(usuario.cpf) +"/update"


    data = {
        "tokenSessao": str(usuario.sessionToken),
        "nome": request.POST.get('nome'),
        "dataDeNascimento": request.POST.get('data_nascimento'),
        "telefone": request.POST.get('telefone'),
    }

    data = json.dumps(data)

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})
    request2.get_method = lambda: 'PUT'

    try:

        acesso_api = Acesso_API()
        acesso_api.API = "clientes"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Atualiza Dados do Usuario"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)
        return minha_conta(request)

    except Exception as e:

        return JsonResponse({'error': e})


def insere_endereco(request):
    endereco = DadosEndereco()

    # Passa o forms como contexto para ser utilizado para obtencao de dados no html
    context = {
        'endereco': endereco,
        'cep_failed': False
    }

    return render(
        request=request,
        template_name='backend/insere_endereco.html',
        context=context
    )

def cadastra_endereco (request):

    try:
        usuario = Usuario.objects.get(email=request.session['usuario'])
    except:
        return dados_cliente(request)

    url = 'http://wsendereco.tk/api/enderecos/cep/'

    endereco = DadosEndereco(data=request.POST)

    url = url + endereco['cep'].value()

    request2 = urllib2.Request(url=url, headers={'Content-Type': 'application/json'})

    try:
        # serializade_data = urllib2.urlopen(request2, data=json.dumps(data))

        acesso_api = Acesso_API()
        acesso_api.API = "endereco"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Buscando Endereco Dado CEP"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        data = {
            'tokenSessao': usuario.sessionToken,
            'cep': endereco['cep'].value(),
            'rua': resposta['Endereco'][0]['logradouro'],
            'numeroCasa':  endereco['numero_casa'].value(),
            'complemento': endereco['complemento'].value(),
            'bairro': resposta['Endereco'][0]['bairro'],
            'cidade': resposta['Endereco'][0]['cidade'],
            'estado': resposta['Endereco'][0]['estado'],
        }
    except Exception as e:
        return JsonResponse({'error': e})

    url = 'http://ec2-18-231-28-232.sa-east-1.compute.amazonaws.com:3002/addresses/'
    url = url + str(usuario.cpf) +"/add"

    data = json.dumps(data)

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    try:

        acesso_api = Acesso_API()
        acesso_api.API = "clientes"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Cadastrando Endereco do Usuario"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)
        return minha_conta(request)
    except Exception as e:
        return JsonResponse({'error': e})


def apagar_conta (request):

    # Passa o forms como contexto para ser utilizado para obtencao de dados no html
    context = {
        "senha_incorreta": False,
    }
    return render (request=request, context=context, template_name="backend/excluir_usuario.html")


def remover_usuario(request):

    senha = request.POST.get("senha")

    try:
        usuario = Usuario.objects.get(email=request.session['usuario'])
    except:
        return dados_cliente(request)

    url = 'http://ec2-18-231-28-232.sa-east-1.compute.amazonaws.com:3002/delete'

    data = {
        "tokenSessao": str(usuario.sessionToken),
        "email": str(usuario.email),
        "senha": senha,
    }

    data = json.dumps(data)

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    try:

        acesso_api = Acesso_API()
        acesso_api.API = "clientes"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Excluindo Cliente"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)
        if "Conta" in resposta['message']:
            usuario.delete()
            return logout(request)
        else:
            context = {
                "senha_incorreta": True,
            }
            return render (request=request, context=context, template_name="backend/excluir_usuario.html")
    except Exception as e:
        return JsonResponse({'error': e})

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
        acesso_api = Acesso_API()
        acesso_api.API = "produtos"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Buscando Todos Produtos"
        acesso_api.save()

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

# Função que busca produto (search)
# Procura por categoria, nome e descrição (NÃO é case sensitive)
def buscar_produto(request):
    nome_produto = request.POST.get('nome_produto')

    produtos = get_produtos(request, pagina='0')

    produtos_busca = []
    for produto in produtos:
        if (nome_produto in produto['category']) or (nome_produto in produto['name']) or (nome_produto in produto['description']):
            produtos_busca.append(produto)

    context = {
            'produtos': produtos_busca,
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

        acesso_api = Acesso_API()
        acesso_api.API = "produtos"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Obtendo Dados do Produto"
        acesso_api.save()

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

        acesso_api = Acesso_API()
        acesso_api.API = "produtos"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Atualizando Produto"
        acesso_api.save()

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

    forms_cartao = DadosCartao(data=request.POST)

    #URL para api de pagamento
    url = 'http://pagamento.4pmv2bgufu.sa-east-1.elasticbeanstalk.com/servico/pagamento_cartao'

    data = {
        "cpf_comprador": "12356712345",
        "valor_compra": "10.20",
        "cnpj_site": "12345678992735",
        "data_emissao_pedido": "2/10/2018",
        "numero_cartao": str(forms_cartao['numero_cartao'].data),
        "nome_cartao": str(forms_cartao['nome_cartao'].data),
        "cvv_cartao": str(forms_cartao['cvv'].data),
        "data_vencimento_cartao": "2/10/2025",
        "credito": "1",
        "num_parcelas": "2"
    }
    print(data)

    data = json.dumps(data)

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    try:

        acesso_api = Acesso_API()
        acesso_api.API = "pagamento"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Compra por Cartao"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        if resposta['pagamento'] == 1:
            vincula_pagamento_pedido(request, resposta['pk_pedido'])
            transforma_carrinho_em_pedido(request)
            return render(request, 'backend/sucesso_pagamento_cartao.html')
        else:
            return render(request, 'backend/falha_pagamento_cartao.html')

    except Exception as e:
        return JsonResponse({'error': e.code})



#Realiza um pagamento por boleto
def pagamento_boleto(request):

    #Recupera os dados do pagamento para enviar para a api de pagamento
    # forms_pagamento = Pagamento(data=request.POST)

    #URL para api de pagamento
    url = 'http://pagamento.4pmv2bgufu.sa-east-1.elasticbeanstalk.com/servico/pagamento_boleto'

    # Variaveis de testebackend/pagamento.html
    now = datetime.now().date()

    valor_compra = request.POST.get('valor_total')
    cnpj = request.POST.get('cnpj')
    credito = request.POST.get('credito')
    cpf = request.POST.get('cpf', '99999999999')

    # data = {
    #     "cpf_comprador": "12356712345",
    #     "valor_compra":"10.20",
    #     "cnpj_site":"12345678992735",
    #     "banco_gerador_boleto":"Itau",
    #     "data_vencimento_boleto":"04/10/2018",
    #     "endereco_fisico_site":"Rua Sindo",
    #     "data_emissao_pedido": "25/06/2018"
    # }
    date = (now+timedelta(days=10)).strftime("%d/%m/%Y")

    data = {
        "cpf_comprador": cpf,
        "valor_compra": valor_compra,
        "cnpj_site": cnpj,
        "banco_gerador_boleto":"Itau",
        "data_vencimento_boleto": str(date),
        "endereco_fisico_site":"Rua Sindo",
        "data_emissao_pedido": now.strftime("%d/%m/%Y")
    }
        # data = {
        #     "cpf_comprador": "12356712345",
        #     "valor_compra": valor_compra,
        #     "cnpj_site": cnpj,
        #     "data_emissao_pedido": now.strftime("%d/%m/%Y"),
        #     "numero_cartao": str(forms_cartao['numero_cartao'].data),
        #     "nome_cartao": str(forms_cartao['nome_cartao'].data),
        #     "cvv_cartao": str(forms_cartao['cvv'].data),
        #     "data_vencimento_cartao": data_vencimento,
        #     "credito": str(credito),
        #     "num_parcelas": str(forms_cartao['num_parcelas'].data),
        # }

    data = json.dumps(data)

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    try:

        acesso_api = Acesso_API()
        acesso_api.API = "pagamento"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Compra por Boleto"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)
        if resposta['status']:
            vincula_pagamento_pedido(request, resposta['pk_pedido'])
            transforma_carrinho_em_pedido(request)
            context = {
                'numero_boleto': resposta['num_boleto']
            }
            return render(request=request, context=context, template_name='backend/sucesso_pagamento_boleto.html')
        else:
            return render(request, 'backend/falha_pagamento_boleto.html')

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

        acesso_api = Acesso_API()
        acesso_api.API = "pagamento"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Busca Dados do Pagamento"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)


        return JsonResponse(resposta)

    except Exception as e:

        return JsonResponse({'error': e.code})

# Chama a página de pagamento
def pagamento(request):
    form_cartao = DadosCartao(data=request.POST)
    valor_total = request.POST.get('valor_total_form', 0)


    try:
        usuario = Usuario.objects.get(email=request.session['usuario'])
        cpf_usuario = usuario.cpf
    except:
        return dados_cliente(request)


    score = get_score(cpf_usuario)['score']

    context = {
        'form_cartao': form_cartao,
        'valor_total': valor_total,
        'score': score,
    }

    return render(request=request, context=context, template_name='backend/pagamento.html')



'''---------------------------------------------------------------------------------------------------------'''
'''-------------------------------------FUNÇÕES DO CARRINHO & PEDIDOS---------------------------------------'''
'''---------------------------------------------------------------------------------------------------------'''


# Dado o id do pagamento, o salva no respectivo carrinho
def vincula_pagamento_pedido(request, id_pagamento):

    try:
        usuario = Usuario.objects.get(email=request.session['usuario'])
    except:
        return dados_cliente(request)

    usuario.carrinho.id_pagamento = id_pagamento
    usuario.carrinho.save()

# Em um pagamento com sucesso, transforma o carrinho em um pedido e gera um novo carrinho para o usuario
def transforma_carrinho_em_pedido(request):
    try:
        usuario = Usuario.objects.get(email=request.session['usuario'])
    except:
        return dados_cliente(request)

    total = 0
    for produto_no_carrinho_obj in usuario.carrinho.produtos_no_carrinho_set.all():
        total += produto_no_carrinho_obj.quantidade * produto_no_carrinho_obj.valor_unitario
    usuario.carrinho.total_carrinho = total
    usuario.carrinho.save()

    pedido = Pedidos()
    pedido.usuario = usuario
    pedido.carrinho = usuario.carrinho
    pedido.save()

    usuario.carrinho = None
    novo_carrinho = Carrinho()
    novo_carrinho.save()
    usuario.carrinho = novo_carrinho
    usuario.save()

#Retorna para o front todos os pedidos de um cliente
def meus_pedidos (request):
    try:
        usuario = Usuario.objects.get(email=request.session['usuario'])
    except:
        return dados_cliente(request)

    pedidos = []

    url_produtos = 'http://ec2-18-218-218-216.us-east-2.compute.amazonaws.com:8080/api/products/'
    url_pagamento = 'http://pagamento.4pmv2bgufu.sa-east-1.elasticbeanstalk.com/servico/busca_pedido'

    for pedido in usuario.pedidos_set.all():
        dados_pedido = {}
        dados_pedido['codigo_pedido'] = pedido.carrinho.id_pagamento
        dados_pedido['total_carrinho'] = (pedido.carrinho.total_carrinho)
        dados_pedido['total_frete'] = (pedido.carrinho.total_frete)

        data = {
            "pk_pagamento": str(pedido.carrinho.id_pagamento)
        }
        data = json.dumps(data)
        request2 = urllib2.Request(url=url_pagamento, data=data, headers={'Content-Type': 'application/json'})
        try:

            acesso_api = Acesso_API()
            acesso_api.API = "pagamento"
            acesso_api.data_acesso = timezone.now()
            acesso_api.descricao = "Busca Dados do Pagamento"
            acesso_api.save()

            serializade_data = urllib2.urlopen(request2).read()
            resposta = json.loads(serializade_data)
        except Exception as e:
            return HttpResponse ("Pk de um pedido não encontrado no módulo de pagamento")

        dados_pedido['dados_pagamento'] = resposta

        produtos=[]
        for produto_no_carrinho in pedido.carrinho.produtos_no_carrinho_set.all():
            url_pedido_atual = url_produtos + str(produto_no_carrinho.produto.id_produto)

            request2 = urllib2.Request(url=url_pedido_atual)

            # Adiciona ao request o login de autorizacao
            basic_auth = base64.b64encode('%s:%s' % ('pagamento', 'LjKDBeqw'))
            request2.add_header("Authorization", "Basic %s" % basic_auth)

            #Realiza uma requisicao ao modulo de produtos para obter os dados do produto
            try:

                acesso_api = Acesso_API()
                acesso_api.API = "produtos"
                acesso_api.data_acesso = timezone.now()
                acesso_api.descricao = "Obtendo Dados do Produto"
                acesso_api.save()

                serializade_data = urllib2.urlopen(request2).read()
                dados_produto = json.loads(serializade_data)
            except Exception as e:
                return JsonResponse({'error': e.code})

            new_dados = {
                'name': dados_produto['name'],
                'description': dados_produto['description'],
                'value': produto_no_carrinho.valor_unitario,
                'quantity': produto_no_carrinho.quantidade,
            }

            produtos.append(new_dados)

        dados_pedido['produtos'] = produtos

        pedidos.append(dados_pedido)

    pedidos = list(reversed(pedidos))

    return pedidos

    # context = {
    #     'pedidos': pedidos
    # }

    # return render (
    #     request=request,
    #     template_name='backend/meus_pedidos.html',
    #     context=context
    # )

# Acessa a pagina do meu carrinho, mostrando um resumo de todos produtos contidos nele
def meu_carrinho(request):
    try:
        usuario = Usuario.objects.get(email=request.session['usuario'])
    except:
        return dados_cliente(request)

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

            acesso_api = Acesso_API()
            acesso_api.API = "produtos"
            acesso_api.data_acesso = timezone.now()
            acesso_api.descricao = "Obtendo Dados do Produto"
            acesso_api.save()

            serializade_data = urllib2.urlopen(request2).read()
            dados_produto = json.loads(serializade_data)
            dados_produto['quantidade_carrinho'] = produto_no_carrinho.quantidade
            produtos.append(dados_produto)
            produto_no_carrinho.valor_unitario = dados_produto['value']
            produto_no_carrinho.save()
        except Exception as e:
            return JsonResponse({'error': e.code})

    # valor_frete = get_valor_frete()
    #
    # usuario.carrinho.total_frete = valor_frete['valor']
    # usuario.carrinho.save()
    context = {
        'produtos': produtos,
        # 'valor_frete': valor_frete
    }

    return render (
        request=request,
        template_name='backend/meu_carrinho.html',
        context=context
    )


# Recebe um produto do front end (id) e o adciona ao carrinho do usuario da sessao atual
def adciona_carrinho(request):

    id_produto = request.POST.get("id_produto")

    try:
        usuario = Usuario.objects.get(email=request.session['usuario'])
    except:
        return dados_cliente(request)

    flag = True
    for produto_no_carrinho_obj in usuario.carrinho.produtos_no_carrinho_set.all():
        if produto_no_carrinho_obj.produto.id_produto == id_produto:
            produto_no_carrinho_obj.quantidade += 1
            produto_no_carrinho_obj.save()
            flag = False

    if flag:
        try:
            produto = Produtos.objects.get(id_produto=id_produto)
        except:
            produto = Produtos()
            produto.id_produto = id_produto
            produto.save()

        produto_no_carrinho = Produtos_no_Carrinho()
        produto_no_carrinho.produto = produto
        produto_no_carrinho.quantidade = 1
        produto_no_carrinho.valor_unitario = -1
        produto_no_carrinho.carrinho = usuario.carrinho
        produto_no_carrinho.save()

    url = 'http://ec2-18-218-218-216.us-east-2.compute.amazonaws.com:8080/api/products/'
    url = url + str(id_produto)

    request2 = urllib2.Request(url=url)
    # Adiciona ao request o login de autorizacao
    basic_auth = base64.b64encode('%s:%s' % ('pagamento', 'LjKDBeqw'))
    request2.add_header("Authorization", "Basic %s" % basic_auth)
    #Realiza uma requisicao ao modulo de produtos para obter os dados do produto
    try:

        acesso_api = Acesso_API()
        acesso_api.API = "produtos"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Obtendo Dados do Produto"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        dados_produto = json.loads(serializade_data)
    except Exception as e:
        return JsonResponse({'error': e.code})

    dados_produto['quantityInStock'] -= 1

    data = json.dumps(dados_produto)
    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})
    request2.get_method = lambda: 'PATCH'
    basic_auth = base64.b64encode('%s:%s' % ('pagamento', 'LjKDBeqw'))
    request2.add_header("Authorization", "Basic %s" % basic_auth)
    #Envia a requsicao ao modulo
    try:

        acesso_api = Acesso_API()
        acesso_api.API = "produtos"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Atualizando Produto"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)
    except Exception as e:
        return JsonResponse({'error': e})

    return meu_carrinho(request)

# Remove um produto do carrinho
def remove_carrinho(request):
    try:
        usuario = Usuario.objects.get(email=request.session['usuario'])
    except:
        return dados_cliente(request)

    id_produto = request.POST.get("id_produto")

    for produto_no_carrinho in usuario.carrinho.produtos_no_carrinho_set.all():
        if (produto_no_carrinho.produto.id_produto == id_produto):

            url = 'http://ec2-18-218-218-216.us-east-2.compute.amazonaws.com:8080/api/products/'
            url = url + str(id_produto)

            request2 = urllib2.Request(url=url)
            # Adiciona ao request o login de autorizacao
            basic_auth = base64.b64encode('%s:%s' % ('pagamento', 'LjKDBeqw'))
            request2.add_header("Authorization", "Basic %s" % basic_auth)
            #Realiza uma requisicao ao modulo de produtos para obter os dados do produto
            try:

                acesso_api = Acesso_API()
                acesso_api.API = "produtos"
                acesso_api.data_acesso = timezone.now()
                acesso_api.descricao = "Obtendo Dados do Produto"
                acesso_api.save()

                serializade_data = urllib2.urlopen(request2).read()
                dados_produto = json.loads(serializade_data)
            except Exception as e:
                return JsonResponse({'error': e.code})

            dados_produto['quantityInStock'] += produto_no_carrinho.quantidade

            data = json.dumps(dados_produto)
            request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})
            request2.get_method = lambda: 'PATCH'
            basic_auth = base64.b64encode('%s:%s' % ('pagamento', 'LjKDBeqw'))
            request2.add_header("Authorization", "Basic %s" % basic_auth)
            #Envia a requsicao ao modulo
            try:

                acesso_api = Acesso_API()
                acesso_api.API = "produtos"
                acesso_api.data_acesso = timezone.now()
                acesso_api.descricao = "Atualizando Produto"
                acesso_api.save()

                serializade_data = urllib2.urlopen(request2).read()
                resposta = json.loads(serializade_data)
            except Exception as e:
                return JsonResponse({'error': e})

            produto_no_carrinho.delete()

    return meu_carrinho(request)

def altera_quantidade (request):
    try:
        usuario = Usuario.objects.get(email=request.session['usuario'])
    except:
        return dados_cliente(request)

    id_produto = request.POST.get("id_produto")
    quantidade = request.POST.get("quantidade")

    #print(Produtos_no_Carrinho.objects.filter(produto__id_produto="7d4acdba-cc6f-4da4-a03b-ce9e7677a6ef", carrinho__usuario = usuario))


    for produto_no_carrinho_obj in usuario.carrinho.produtos_no_carrinho_set.all():
        if produto_no_carrinho_obj.produto.id_produto == id_produto:
            dif = int(quantidade) - produto_no_carrinho_obj.quantidade
            produto_no_carrinho_obj.quantidade = quantidade
            produto_no_carrinho_obj.save()

            url = 'http://ec2-18-218-218-216.us-east-2.compute.amazonaws.com:8080/api/products/'
            url = url + str(id_produto)

            request2 = urllib2.Request(url=url)
            # Adiciona ao request o login de autorizacao
            basic_auth = base64.b64encode('%s:%s' % ('pagamento', 'LjKDBeqw'))
            request2.add_header("Authorization", "Basic %s" % basic_auth)
            #Realiza uma requisicao ao modulo de produtos para obter os dados do produto
            try:

                acesso_api = Acesso_API()
                acesso_api.API = "produtos"
                acesso_api.data_acesso = timezone.now()
                acesso_api.descricao = "Obtendo Dados do Produto"
                acesso_api.save()

                serializade_data = urllib2.urlopen(request2).read()
                dados_produto = json.loads(serializade_data)
            except Exception as e:
                return JsonResponse({'error': e.code})

            dados_produto['quantityInStock'] -= dif

            data = json.dumps(dados_produto)
            request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})
            request2.get_method = lambda: 'PATCH'
            basic_auth = base64.b64encode('%s:%s' % ('pagamento', 'LjKDBeqw'))
            request2.add_header("Authorization", "Basic %s" % basic_auth)
            #Envia a requsicao ao modulo
            try:

                acesso_api = Acesso_API()
                acesso_api.API = "produtos"
                acesso_api.data_acesso = timezone.now()
                acesso_api.descricao = "Atualizando Produto"
                acesso_api.save()

                serializade_data = urllib2.urlopen(request2).read()
                resposta = json.loads(serializade_data)
            except Exception as e:
                return JsonResponse({'error': e})

    resposta = {
        "sucesso": 1
    }

    return JsonResponse(resposta)

'''---------------------------------------------------------------------------------------------------------'''
'''--------------------------------------------API DE LOGISTICA---------------------------------------------'''
'''---------------------------------------------------------------------------------------------------------'''

#Funcao que pega o valor de frete da api de logistica
def get_valor_frete(request):

    try:
        usuario = Usuario.objects.get(email=request.session['usuario'])
    except:
        return dados_cliente(request)

    #URL para acesso da api (VAI PRECISAR SER ALTERADA DEPOIS)
    url = 'https://shielded-caverns-17296.herokuapp.com/frete'

    #Pega o cep do cliente passado por um post, por meio do id 'cep'
    cep = request.POST.get('cep')
    numero_residencia = request.POST.get('numero_residencia')
    complemento = request.POST.get('complemento')

    data = {
        'CEP': cep
    }

    data = json.dumps(data)

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    try:

        acesso_api = Acesso_API()
        acesso_api.API = "logistica"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Calculo do Valor do Frete"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        usuario.carrinho.cep = cep
        usuario.carrinho.numero_residencia = numero_residencia
        usuario.carrinho.complemento = complemento
        usuario.carrinho.save()

        return JsonResponse(resposta)

    except Exception as e:

        return JsonResponse({'error': e})


'''---------------------------------------------------------------------------------------------------------'''
'''---------------------------------------------API DE CRÉDITO----------------------------------------------'''
'''---------------------------------------------------------------------------------------------------------'''

#Funcao que pega o score de um cliente na api de credito
def get_score(cpf):

    #Pega o cpf do cliente passado no momento do pagamento
    #cpf = request.POST.get('cpf')
    if not cpf:
        cpf=str("20314520369")
    # URL para acesso da api de credito
    url = 'http://ec2-54-233-234-42.sa-east-1.compute.amazonaws.com:3000/api/v1/score/' + cpf

    request2 = urllib2.Request(url=url)

    try:
        acesso_api = Acesso_API()
        acesso_api.API = "credito"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Obtem Score do Cliente"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        #return JsonResponse(resposta)
        return resposta

    except Exception as e:

        return JsonResponse({'error': e})

'''---------------------------------------------------------------------------------------------------------'''
'''-----------------------------------------------PAGINA ADM------------------------------------------------'''
'''---------------------------------------------------------------------------------------------------------'''

def acesso_apis(request):

    data_inicio=request.POST.get("data_inicio")
    data_final=request.POST.get("data_final")
    if data_inicio != None:
        data_final = datetime.strptime(data_final, "%Y-%m-%d").date()
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        flag = False
    else:
        flag = True

    clientes = []
    enderecos = []
    produtos = []
    pagamentos = []
    logisticas = []
    creditos = []
    for acesso in Acesso_API.objects.all():
        if flag or (acesso.data_acesso >= data_inicio and acesso.data_acesso <= data_final):
            data = {
                "data_acesso": acesso.data_acesso,
                "descricao": acesso.descricao,
            }
            if acesso.API == "endereco":
                enderecos.append(data)
            if acesso.API == "clientes":
                clientes.append(data)
            if acesso.API == "produtos":
                produtos.append(data)
            if acesso.API == "pagamento":
                pagamentos.append(data)
            if acesso.API == "logistica":
                logisticas.append(data)
            if acesso.API == "credito":
                creditos.append(data)

    context = {
        "clientes": clientes,
        "enderecos": enderecos,
        "produtos": produtos,
        "pagamentos": pagamentos,
        "logisticas": logisticas,
        "creditos":creditos,
    }

    return render (request = request, context=context, template_name="backend/acesso_apis.html")

def mostra_todos_produtos(request):
    produtos = get_produtos(request)

    context = {
        "produtos": produtos,
    }

    return render (request=request, context=context, template_name="backend/todos_produtos.html")

def altera_produto(request):

    id_produto = request.POST.get("id_produto")
    print (id_produto)

    url = 'http://ec2-18-218-218-216.us-east-2.compute.amazonaws.com:8080/api/products/'
    url = url + str(id_produto)

    request2 = urllib2.Request(url=url)
    # Adiciona ao request o login de autorizacao
    basic_auth = base64.b64encode('%s:%s' % ('pagamento', 'LjKDBeqw'))
    request2.add_header("Authorization", "Basic %s" % basic_auth)
    #Realiza uma requisicao ao modulo de produtos para obter os dados do produto
    try:

        acesso_api = Acesso_API()
        acesso_api.API = "produtos"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Obtendo Dados do Produto"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        dados_produto = json.loads(serializade_data)
    except Exception as e:
        return JsonResponse({'error': e.code})

    context = {
        "produto": dados_produto,
    }

    return render (request=request, context=context, template_name="backend/altera_produto.html")

def altera_dados_produto(request):

    id_produto = request.POST.get("id_produto")

    url = 'http://ec2-18-218-218-216.us-east-2.compute.amazonaws.com:8080/api/products/'
    url = url + str(id_produto)

    request2 = urllib2.Request(url=url)
    # Adiciona ao request o login de autorizacao
    basic_auth = base64.b64encode('%s:%s' % ('pagamento', 'LjKDBeqw'))
    request2.add_header("Authorization", "Basic %s" % basic_auth)
    #Realiza uma requisicao ao modulo de produtos para obter os dados do produto
    try:

        acesso_api = Acesso_API()
        acesso_api.API = "produtos"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Obtendo Dados do Produto"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        dados_produto = json.loads(serializade_data)
    except Exception as e:
        return JsonResponse({'error': e.code})


    dados_produto['name'] = request.POST.get("name")
    dados_produto['description'] = request.POST.get("description")
    dados_produto['weight'] = request.POST.get("weight")
    dados_produto['category'] = request.POST.get("category")
    dados_produto['type'] = request.POST.get("type")
    dados_produto['manufacturer'] = request.POST.get("manufacturer")
    dados_produto['quantityInStock'] = request.POST.get("quantityInStock")
    dados_produto['value'] = request.POST.get("value")
    dados_produto['promotionalValue'] = request.POST.get("promotionalValue")
    dados_produto['availableToSell'] = request.POST.get("availableToSell")
    dados_produto['onSale'] = request.POST.get("onSale")


    url = 'http://ec2-18-218-218-216.us-east-2.compute.amazonaws.com:8080/api/products/' + str(id_produto)

    data = json.dumps(dados_produto)
    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})
    request2.get_method = lambda: 'PATCH'

    basic_auth = base64.b64encode('%s:%s' % ('pagamento', 'LjKDBeqw'))
    request2.add_header("Authorization", "Basic %s" % basic_auth)

    #Envia a requsicao ao modulo
    try:

        acesso_api = Acesso_API()
        acesso_api.API = "produtos"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Atualizando Produto"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

    except Exception as e:

        return JsonResponse({'error': e})


    # url = 'http://ec2-18-218-218-216.us-east-2.compute.amazonaws.com:8080/api/products/' + str(id_produto) + "/images"
    #
    # imagens = {
    #     "imageUrls": [request.POST.get("images")]
    # }
    #
    # data = json.dumps(imagens)
    # request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})
    #
    # basic_auth = base64.b64encode('%s:%s' % ('pagamento', 'LjKDBeqw'))
    # request2.add_header("Authorization", "Basic %s" % basic_auth)
    #
    # #Envia a requsicao ao modulo
    # try:
    #
    #     acesso_api = Acesso_API()
    #     acesso_api.API = "produtos"
    #     acesso_api.data_acesso = timezone.now()
    #     acesso_api.descricao = "Altera Imagem Produto"
    #     acesso_api.save()
    #
    #     serializade_data = urllib2.urlopen(request2).read()
    #     resposta = json.loads(serializade_data)
    #
    # except Exception as e:
    #
    #     return JsonResponse({'error': e})

    return mostra_todos_produtos(request)

def cadastrar_produto(request):

    return render (request=request, context={}, template_name="backend/cadastrar_produto.html")

def cadastra_produto_api(request):
    url = 'http://ec2-18-218-218-216.us-east-2.compute.amazonaws.com:8080/api/products/'

    dados_produto = {}

    dados_produto['name'] = request.POST.get("name")
    dados_produto['description'] = request.POST.get("description")
    dados_produto['weight'] = request.POST.get("weight")
    dados_produto['category'] = request.POST.get("category")
    dados_produto['type'] = request.POST.get("type")
    dados_produto['manufacturer'] = request.POST.get("manufacturer")
    dados_produto['quantityInStock'] = request.POST.get("quantityInStock")
    dados_produto['value'] = request.POST.get("value")
    dados_produto['promotionalValue'] = request.POST.get("promotionalValue")
    dados_produto['availableToSell'] = request.POST.get("availableToSell")
    dados_produto['onSale'] = request.POST.get("onSale")

    data = json.dumps(dados_produto)
    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})
    # Adiciona ao request o login de autorizacao
    basic_auth = base64.b64encode('%s:%s' % ('pagamento', 'LjKDBeqw'))
    request2.add_header("Authorization", "Basic %s" % basic_auth)
    #Realiza uma requisicao ao modulo de produtos para obter os dados do produto
    try:

        acesso_api = Acesso_API()
        acesso_api.API = "produtos"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Cadastrando Produto"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        dados_produto = json.loads(serializade_data)
    except Exception as e:
        return JsonResponse({'error': e.code})

    url = 'http://ec2-18-218-218-216.us-east-2.compute.amazonaws.com:8080/api/products/' + str(dados_produto['id']) + "/images"

    imagens = {
        "imageUrls": [request.POST.get("images")]
    }

    data = json.dumps(imagens)
    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})

    basic_auth = base64.b64encode('%s:%s' % ('pagamento', 'LjKDBeqw'))
    request2.add_header("Authorization", "Basic %s" % basic_auth)

    #Envia a requsicao ao modulo
    try:

        acesso_api = Acesso_API()
        acesso_api.API = "produtos"
        acesso_api.data_acesso = timezone.now()
        acesso_api.descricao = "Altera Imagem Produto"
        acesso_api.save()

        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

    except Exception as e:

        return JsonResponse({'error': e})

    return mostra_todos_produtos(request)
