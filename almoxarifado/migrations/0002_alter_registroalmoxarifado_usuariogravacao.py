# Generated by Django 5.1.1 on 2024-11-12 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('almoxarifado', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registroalmoxarifado',
            name='usuariogravacao',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
