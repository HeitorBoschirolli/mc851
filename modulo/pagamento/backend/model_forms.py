from django import forms

class DadosCliente(forms.Form):
    nome_cliente = forms.CharField(
        label="Nome do Cliente", 
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'type': 'name',
                'class': 'form-control',
                'placeholder': "Nome",
                'required': True
            },
        )
    )
    email = forms.CharField(label="Email", max_length=100, widget=forms.TextInput(
        attrs={
            'type': 'email',
            'class': 'form-control',
            'placeholder': "Exemplo: email@email.com",
        }
    ))
    senha = forms.CharField(label="Senha", max_length=100, widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'form-control',
            'placeholder': "Senha",
            'required': True
        }
    ))
    cpf = forms.CharField(
        label="CPF", 
        max_length=11, 
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'pattern': '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]',
                'placeholder': "Exemplo: 12345678912",
                'required': True,
                'title': 'Example: 12312312312'
            }
        ),
        # error_message='sdfhsakdf'
    )
    data_nascimento = forms.CharField(
        label="Data de Nascimento", 
        max_length=100, 
        widget=forms.TextInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': "Exemplo: 01/01/2000",
                'required': True
            },
        )
    )
    telefone = forms.CharField(label="Telefone", max_length=9, widget=forms.TextInput(
        attrs={
            'type': 'tel',
            'class': 'form-control',
            'placeholder': "Exemplo: 123456789",
        }
    ))
    id_grupo = forms.CharField(label="Id do Grupo", max_length=100, widget=forms.TextInput(
        attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': "Exemplo: 1"
        }
    ))

class DadosEndereco(forms.Form):
    id = forms.IntegerField(label="Id do Endereco")
    cep = forms.CharField(label="CEP", max_length=8, widget=forms.TextInput(
        attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Exemplo: 00000001'
        }
    ))
    logradouro = forms.CharField(label="Logradouro", max_length=100)
    inicio = forms.CharField(label="Inicio", max_length=50)
    fim = forms.CharField(label="Fim", max_length=50)
    latitude = forms.CharField(label="Latitude", max_length=12)
    longitude = forms.CharField(label="Longitude", max_length=12)
    bairro = forms.CharField(label="Bairro", max_length=100)
    cidade = forms.CharField(label="Cidade", max_length=100)
    estado = forms.CharField(label="Estado", max_length=2)
    numero_casa = forms.IntegerField(label="Numero da Casa", widget=forms.TextInput(
        attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Exemplo: 175'
        }
    ))
    complemento = forms.CharField(label="Complemento", max_length=200, widget=forms.TextInput(
        attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Exemplo: ap. 101'
        }
    ))