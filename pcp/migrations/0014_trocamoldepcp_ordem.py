# Generated by Django 5.1.1 on 2024-12-04 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcp', '0013_alter_trocamoldepcp_molde_maquina_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trocamoldepcp',
            name='ordem',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
