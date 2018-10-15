from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^home', views.home, name='home'),

    #Pega os dados do cliente para realizar um cadastro
    url(r'^cadastro', views.cadastro, name='cadastro'),
    url(r'^dados_cliente', views.dados_cliente, name='dados_cliente'),
    #Faz uma requisicao para a api de clientes, para realizar o cadastro do cliente
    url(r'^cadastra_cliente', views.cadastra_cliente, name='cadastra_cliente'),

    #Confirma o registro de um cliente
    url(r'^confirma_cadastro', views.confirma_cadastro, name='confirma_cadastro'),

    # efetua login de um cliente
    url(r'^login', views.dados_login, name='login'),
    url(r'^resultado_login', views.resultado_login, name='resultado_login'),


    #API de Endereco

    #Pega do html, o cep para pesquisa do endereco
    url(r'^get_cep', views.get_cep, name='endereco_por_cep'),
    #Faz uma requisicao do endereco pelo cep, na api de Enderecos
    url(r'^endereco_cep', views.endereco_cep, name='endereco_por_cep_api'),
]