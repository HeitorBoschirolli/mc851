# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(dados):

    import pdb
    pdb.set_trace()

    fromaddr = "mc851nani@gmail.com"
    toaddr = "mc851nani@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Dados da Compra"

    body = "Total da Compra: R${}\n".format(dados['total_compra']) + \
           "Valor do Carrinho: R${}\n".format(dados['total_carrinho']) + \
           "Valor do Frete: R${}\n".format(dados['total_frete']) + \
           "CEP da Entrega: {}\n".format(dados['cep_entrega']) + \
           "Número da Residência: {}.\n".format(dados['numero_residencia']) + \
           "Complemento: {}\n".format(dados['complemento']) + \
           "Tempo para Entrega: {} Dias\n".format(dados['tempo_entrega']) + \
           "Produtos:\n"

    for i in dados['produtos']:

        body += "   - Nome do Produto: {}:\n".format(i['nome'].encode('utf-8'))
        body += "       - Quantidade: {}\n".format(i['quantidade'])
        body += "       - Preço: R${}\n".format(i['valor'])

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "mc851pagamento")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()