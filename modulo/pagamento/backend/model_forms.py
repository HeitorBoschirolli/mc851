from django import forms

class DadosCliente(forms.Form):
    nome_cliente = forms.CharField(label="Nome do Cliente", max_length=100)
    email = forms.CharField(label="Email", max_length=100)
    senha = forms.CharField(label="Senha", max_length=100)
    cpf = forms.CharField(label="CPF", max_length=11)
    data_nascimento = forms.CharField(label="Data de Nascimento", max_length=100)
    telefone = forms.CharField(label="Telefone", max_length=100)
    id_grupo = forms.CharField(label="Id do Grupo", max_length=100)

class DadosEndereco(forms.Form):
    id = forms.IntegerField(label="Id do Endereco")
    cep = forms.CharField(label="CEP", max_length=8)
    logradouro = forms.CharField(label="Logradouro", max_length=100)
    inicio = forms.CharField(label="Inicio", max_length=50)
    fim = forms.CharField(label="Fim", max_length=50)
    latitude = forms.CharField(label="Latitude", max_length=12)
    longitude = forms.CharField(label="Longitude", max_length=12)
    bairro = forms.CharField(label="Bairro", max_length=100)
    cidade = forms.CharField(label="Cidade", max_length=100)
    estado = forms.CharField(label="Estado", max_length=2)