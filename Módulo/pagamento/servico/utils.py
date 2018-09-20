import datetime


def corretude_cpf (cpf):
    cpf = str(cpf)
    
    if not cpf.isdigit():
        return -2 # o cpf nao contem somente digitos
    
    if len(cpf) != 11:
        return -3 # o cpf tem tamanho invalido
    
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


def corretude_endereco_fisico (endereco):
    return 0
