# Generated by Django 2.1.1 on 2018-09-02 23:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_boleto_cartao_cliente_pedido'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
