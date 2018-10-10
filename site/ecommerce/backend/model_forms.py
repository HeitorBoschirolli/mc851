from django import forms

class DadosCliente(forms.Form):
    nome_cliente = forms.CharField(label="Nome do Cliente", max_length=100)
    email = forms.CharField(label="Email", max_length=100)
    senha = forms.CharField(label="Senha", max_length=100)
    cpf = forms.CharField(label="CPF", max_length=11)
    data_nascimento = forms.CharField(label="Data de Nascimento", max_length=100)
    telefone = forms.CharField(label="Telefone", max_length=100)
    id_grupo = forms.CharField(label="Id do Grupo", max_length=100)