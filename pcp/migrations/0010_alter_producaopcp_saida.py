# Generated by Django 5.1.1 on 2024-11-19 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcp', '0009_producaopcp_falta_producaopcp_pedido_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producaopcp',
            name='saida',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
