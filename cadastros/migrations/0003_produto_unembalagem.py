# Generated by Django 5.1.1 on 2024-11-08 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0002_produto_embalagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='unembalagem',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]