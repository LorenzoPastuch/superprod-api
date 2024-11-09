# Generated by Django 5.1.1 on 2024-11-09 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcp', '0002_alter_soldapcp_cor_1_alter_soldapcp_cor_2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producaopcp',
            old_name='quantidade',
            new_name='unidades',
        ),
        migrations.AddField(
            model_name='producaopcp',
            name='kilogramas',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
