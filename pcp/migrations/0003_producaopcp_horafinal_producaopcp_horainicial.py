# Generated by Django 5.1.1 on 2024-10-29 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcp', '0002_producaopcp_caixas'),
    ]

    operations = [
        migrations.AddField(
            model_name='producaopcp',
            name='horafinal',
            field=models.DateTimeField(default='2024-01-01T00:00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producaopcp',
            name='horainicial',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
