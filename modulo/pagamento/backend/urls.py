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
    #adciona item ao carrinho
    url(r'^adciona_carrinho', views.adciona_carrinho, name='adciona_carrinho'),
    #remove item ao carrinho
    url(r'^remove_carrinho', views.remove_carrinho, name='remove_carrinho'),
    #procura produto (search)
    url(r'^buscar_produto', views.buscar_produto, name='buscar_produto'),
    # URL para pagamento (quando clica em pagar em "Meu Carrinho")
    url(r'^pagamento/$', views.pagamento, name='pagamento'),
    # URL para ver todos pedidos feitos por um usuario
    url(r'^meus_pedidos', views.meus_pedidos, name='meus_pedidos'),
    # URL para atualizar o meu carrinho no banco de dados
    url(r'^altera_quantidade', views.altera_quantidade, name='meus_pedidos'),
    # URL para checar os acessos as API's
    url(r'^acesso_apis', views.acesso_apis, name='acesso_apis'),
    # URL para mostrar todos produtos para alteração
    url(r'^mostra_todos_produtos', views.mostra_todos_produtos, name='mostra_todos_produtos'),
    # URL para inserir dados do produto que será alterado
    url(r'^altera_produto', views.altera_produto, name='altera_produto'),
    # URL para alterar na API os dados do produto
    url(r'^altera_dados_produto', views.altera_dados_produto, name='altera_dados_produto'),
    # URL para mostar form para cadastrar produto
    url(r'^cadastrar_produto', views.cadastrar_produto, name='cadastrar_produto'),
    # URL para cadastrar o produto na api de fato
    url(r'^cadastra_produto_api', views.cadastra_produto_api, name='cadastra_produto_api'),

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

    # Alterar dados cadastrais
    url(r'^alterar_dados_cadastrais', views.alterar_dados_cadastrais, name='alterar_dados_cadastrais'),

    #Executa a ação de alterar os dados
    url(r'^altera_dados', views.altera_dados, name='altera_dados'),

    #Pagina que pede senha para excluir usuario
    url(r'^apagar_conta', views.apagar_conta, name='apagar_conta'),

    #Executa a ação de alterar os dados
    url(r'^remover_usuario', views.remover_usuario, name='remover_usuario'),


    #---------------------------------------------------------------------------------------------------------#
    #---------------------------------------------API DE ENDERECO---------------------------------------------#
    #---------------------------------------------------------------------------------------------------------#

    #Pega do html, o cep para pesquisa do endereco
    url(r'^endereco_cliente', views.endereco_cliente, name='endereco_cliente'),
    #Faz uma requisicao do endereco pelo cep, na api de Enderecos
    url(r'^endereco_cep', views.endereco_cep, name='endereco_por_cep_api'),
    #Insere novo endereço para aquele cliente
    url(r'^insere_endereco', views.insere_endereco, name='insere_endereco'),
    #Cadastra junto a api de cliente aquele endereço
    url(r'^cadastra_endereco', views.cadastra_endereco, name='cadastra_endereco'),

    #---------------------------------------------------------------------------------------------------------#
    #---------------------------------------------API DE PRODUTOS---------------------------------------------#
    #---------------------------------------------------------------------------------------------------------#

    #busca por produtos
    url(r'^produtos/(?P<categoria>[a-zA-Z]+)/(?P<pagina>[0-9]+)', views.produtos, name='produtos'),
    #Renderiza pagina onde o admin colocara os dados para atualizar um produto
    url(r'^dados_produto', views.render_att_produtos, name='dados_produto'),
    #Link para atualizacao de dados do produto
    url(r'^att_dados_produto', views.att_produto, name='att_dados_produto'),


    # ---------------------------------------------------------------------------------------------------------#
    # --------------------------------------------API DE PAGAMENTO---------------------------------------------#
    # ---------------------------------------------------------------------------------------------------------#

    # URL para cadastrar um pagamento por cartão
    url(r'^pagamento_cartao', views.pagamento_cartao, name='pagamento_cartao'),

    # URL para cadastrar um pagamento por boleto
    url(r'^pagamento_boleto', views.pagamento_boleto, name='pagamento_boleto'),

    # URL para consulta de um pagamento por PK
    url(r'^consulta_pagamento', views.consulta_pagamento, name='consulta_pagamento'),



    # ---------------------------------------------------------------------------------------------------------#
    # --------------------------------------------API DE LOGISTICA---------------------------------------------#
    # ---------------------------------------------------------------------------------------------------------#

    # URL para consulta de valor de frete para um determinado cep
    url(r'^get_valor_frete', views.get_valor_frete, name='get_valor_frete'),


    # ---------------------------------------------------------------------------------------------------------#
    # ---------------------------------------------API DE CRÉDITO----------------------------------------------#
    # ---------------------------------------------------------------------------------------------------------#

    # URL para consulta de um score de um cliente
    url(r'^get_score', views.get_score, name='get_score'),
]
