from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *
from .model_forms import *
from .utils import *


def index(request):
    return HttpResponse("Hello, world. You're at the payment index.")

def pagamento_boleto(request):
    form_cartao = PagamentoForm()
    context = {
        'form_cartao': form_cartao,
    }
    return render(request, 'servico/get_infos_boleto.html', context)

def status_boleto(request):
    form_boleto = PagamentoForm(data=request.POST)

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
        'status_cpf_comprador': status_cpf_comprador,
        'status_valor_compra': status_valor_compra,
        'status_cnpj_site': status_cnpj_site,
        'status_banco_gerador_boleto': status_banco_gerador_boleto,
        'status_data_vencimento_boleto': status_data_vencimento_boleto,
        'status_endereco_fisico_site': status_endereco_fisico_site,
    }
    return render(request, 'servico/status_boleto.html', context)