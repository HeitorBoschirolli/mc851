from django.conf.urls import url

from . import views

urlpatterns = [

    #Home do site
    url(r'^home', views.home, name='home'),

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

    #busca por eletromesticos
    url(r'^produtos_eletrodomesticos/(?P<pagina>[0-9]+)', views.produtos_eletrodomesticos, name='produtos_eletrodomesticos'),
    #busca por computadores
    url(r'^produtos_computadores/(?P<pagina>[0-9]+)', views.produtos_computadores, name='produtos_computadores'),
    #busca por celulares
    url(r'^produtos_celulares/(?P<pagina>[0-9]+)', views.produtos_celulares, name='produtos_celulares'),


]
