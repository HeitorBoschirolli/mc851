# Generated by Django 2.1 on 2018-09-17 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servico', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartao',
            name='debito',
        ),
        migrations.AlterField(
            model_name='pedido',
            name='cnpj_empresa',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='cpf_cliente',
            field=models.CharField(max_length=15),
        ),
    ]