import numpy as np


def buscapagamentos(id):
    '''Abre o arquivo BancoDeDados que possui todos os dados de pagamento dos id's fornecidos'''
    file = open('/home/vaoki/ec/mc851/mc851/servidor/mysite/polls/BancoDeDados.txt')

    '''Armazena os pagamentos em uma lista'''
    pagamentos = file.readlines()

    for i in pagamentos:

        id_local = i.split('-')[0]

        if(id == id_local):
            return i.split('-')[1]

    return "ID do pagamento não encontrado"
