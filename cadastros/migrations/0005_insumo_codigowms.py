# Generated by Django 5.1.1 on 2024-11-12 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0004_log_cadastro_insumo'),
    ]

    operations = [
        migrations.AddField(
            model_name='insumo',
            name='codigowms',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]