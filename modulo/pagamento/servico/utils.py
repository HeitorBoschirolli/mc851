# -*- coding: utf-8 -*-

import datetime
import random
from .models import *


def corretude_cpf (cpf):
    """
    Verifica se um cpf está formatado corretamente, isto é, possui 11 caracteres
    numéricos.

    Parâmetros
    ----------
    cpf : str ou unicode
        CPF cuja formatação será verificada.

    Retornos
    ----------
    status_cpf : int
        Código indicando se o cpf está formatado corretamente (0) ou
        não (-2 ou -3).
        -2 indica que o CPF passado possui um ou mais caracteres que não são
        numéricos.
        -3 indica que o tamanho do CPF passado está incorreto, ou seja, que ele
        não possui 11 dígitos como deveria.
    """
    cpf = str(cpf)

    if not cpf.isdigit():
        return -2

    if len(cpf) != 11:
        return -3

    return 0

def corretude_valor (valor):
    valor = str(valor)

    parte_inteira = valor[:]
    parte_real = '00'
    for index, digit in enumerate(valor):
        if digit == '.':
            parte_inteira = valor[:index]
            parte_real = valor[index + 1:]

    if not parte_inteira.isdigit():
        return -2 # tem algo que nao eh um numero
    if not parte_real.isdigit() and len(parte_real) > 0:
        return -2 # tem algo que nao eh um numero
    if len(parte_real) > 2:
        return -3 # mais de duas casas decimais

    return 0

def corretude_banco (banco):
    banco = str(banco)

    # if type(banco) != str:
    #     return -1 # o tipo passado esta incorreto

    if not banco.isalpha():
        return -2 # contem caracteres que nao sao letras

    return 0

def formata_banco (banco):
    banco = str(banco)
    return banco.lower()


def corretude_cnpj (cnpj):
    # if type(cnpj) != str:
    #     return -1 # o tipo passado esta incorreto
    cnpj = str(cnpj)

    if not cnpj.isdigit():
        return -2 # o cnpj nao contem somente digitos

    if len(cnpj) != 14:
        return -3 # o cnpj tem tamanho invalido

    return 0


def corretude_data (data):
    # if type(data) != str:
    #     return -1 # o tipo passado esta incorreto
    data = str(data)

    try:
        datetime.datetime.strptime(data, '%d/%m/%Y')
    except ValueError:
        return -2 # data no formato errado

    return 0


# Verifica se a data do cartão está no formato correto e se o cartão não está vencido
# INPUT:
#   data
# OUTPUT:
#    0 --> Data correta e válida
#   -1 --> Data no formato correto porém cartão já vencido
#   -2 --> Data no formato incorreto
def corretude_data_vencimento_cartao (data_vencimento_str):
    status = corretude_data(data_vencimento_str)
    if status != -2: # data está no formato correto
        data_vencimento = datetime.datetime.strptime(data_vencimento_str, '%d/%m/%Y')
        if datetime.datetime.now() < data_vencimento:
            return 0 # Data no formato correto e não está vencido
        else:
            return -1 # Data no formato correto porém vencido
    else:
        return status # Data no formato incorreto





def corretude_endereco_fisico (endereco):
    return 0


def gera_boleto(cpf_comprador, valor_compra, cnpj_site, banco,
                data_vencimento, endereco_empresa,
                nome_empresa="nao precisa ter isso"):
    status_boleto = 2 # esperando pagamento ser efetuado

    data_emissao_pedido = datetime.datetime.now()

    num_boleto = str(random.randint(1000000000, 9999999999))
    num_boleto += str(random.randint(10000000000, 99999999999))
    num_boleto += str(random.randint(10000000000, 99999999999))
    num_boleto += str(random.randint(10000000000000, 99999999999999))

    pedido = Pedido(cpf_cliente=cpf_comprador,
                    cnpj_empresa=cnpj_site,
                    valor=valor_compra,
                    data_emissao_pedido=data_emissao_pedido)
    pedido.save()

    data_vencimento = datetime.datetime.strptime(data_vencimento, "%d/%m/%Y")

    boleto = Boleto(banco=banco,
                    num_boleto=num_boleto,
                    data_vencimento_boleto=data_vencimento,
                    nome_empresa=nome_empresa,
                    endereco_empresa=endereco_empresa,
                    status_boleto=status_boleto,
                    pedido=pedido)
    boleto.save()

    return num_boleto


def corretude_numero_cartao (numero_cartao):
    numero_cartao = str(numero_cartao)

    if not numero_cartao.isdigit():
        return -2 # o numero_cartao nao contem somente digitos

    if len(numero_cartao) != 16:
        return -3 # o numero_cartao tem tamanho invalido

    return 0


def corretude_cvv (cvv):
    cvv = str(cvv)

    if not cvv.isdigit():
        return -2 # o cvv nao contem somente digitos

    if len(cvv) != 3:
        return -3 # o cvv tem tamanho invalido

    return 0


def corretude_nome_impresso_cartao (nome_impresso_cartao):
    nome_impresso_cartao = str(nome_impresso_cartao)

    if not nome_impresso_cartao.isalpha():
        return -2 # contem caracteres que nao sao letras

    return 0


def corretude_tipo_cartao (credito):
    if credito:
        credito = int(credito)
    else:
        return -1 # Forma de pagamento não escolhida

    if credito not in [0,1]:
        return -2 # Opcao de pagamento inválida
    return 0

def corretude_num_parcelas (num_parcelas):
    try:
        num_parcelas = int(num_parcelas)
    except:
        return -1 # o num_parcelas nao contem somente digitos

    if num_parcelas <= 0:
        return -2 # número de parcelas inválido
    return 0
