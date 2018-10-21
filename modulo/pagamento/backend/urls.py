# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [

    #Home do site
    url(r'^home', views.home, name='home'),
    #desloga o usuario
    url(r'^logout', views.logout, name='desloga_usuario'),
    # Página da conta do usuário
    url(r'^minha_conta', views.minha_conta, name='minha_conta'),
    # Página do meu carrinho
    url(r'^meu_carrinho', views.meu_carrinho, name='meu_carrinho'),

    #---------------------------------------------------------------------------------------------------------#
    #---------------------------------------------API DE CLIENTES---------------------------------------------#
    #---------------------------------------------------------------------------------------------------------#

    # pega os dados do cliente para concluir o cadastro
    url(r'^dados_cliente', views.dados_cliente, name='dados_cliente'),
    #Faz uma requisicao para a api de clientes, para realizar o cadastro do cliente
    url(r'^cadastra_cliente', views.cadastra_cliente, name='cadastra_cliente'),
    #Confirma o registro de um clienste
    url(r'^confirma_cadastro', views.confirma_cadastro, name='confirma_cadastro'),

    # Efetua login de um cliente
    url(r'^login', views.login, name='login'),
    url(r'^resultado_login', views.resultado_login, name='resultado_login'),

    # Recuperar senha
    url(r'^recuperar', views.recuperar, name='recuperar'),


    #---------------------------------------------------------------------------------------------------------#
    #---------------------------------------------API DE ENDERECO---------------------------------------------#
    #---------------------------------------------------------------------------------------------------------#

    #Pega do html, o cep para pesquisa do endereco
    url(r'^endereco_cliente', views.endereco_cliente, name='endereco_cliente'),
    #Faz uma requisicao do endereco pelo cep, na api de Enderecos
    url(r'^endereco_cep', views.endereco_cep, name='endereco_por_cep_api'),

    #---------------------------------------------------------------------------------------------------------#
    #---------------------------------------------API DE PRODUTOS---------------------------------------------#
    #---------------------------------------------------------------------------------------------------------#

    #busca por produtos
    url(r'^produtos/(?P<categoria>[a-zA-Z]+)/(?P<pagina>[0-9]+)', views.get_produtos, name='produtos'),
    #Renderiza pagina onde o admin colocara os dados para atualizar um produto
    url(r'^dados_produto', views.render_att_produtos, name='dados_produto'),
    #Link para atualizacao de dados do produto
    url(r'^att_dados_produto', views.att_produto, name='att_dados_produto'),

    url(r'^pagamento/', views.pagamento, name='pagamento'),


]
