# Generated by Django 5.1.1 on 2024-11-14 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0005_insumo_codigowms'),
        ('pcp', '0006_alter_embaladorespcp_embalador_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='embaladorespcp',
            name='setor',
            field=models.CharField(blank=True, choices=[('INJETORA', 'INJETORA'), ('SOLDA ULTRASSOM', 'SOLDA ULTRASSOM'), ('EXTRUSORA', 'CANUDOS')], max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='CanudoPcp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tamanho', models.CharField(max_length=10)),
                ('quantidade', models.IntegerField()),
                ('ordem', models.IntegerField()),
                ('status', models.CharField(choices=[('FILA P/ PRODUZIR', 'FILA P/ PRODUZIR'), ('EM PRODUÇÃO', 'EM PRODUÇÃO'), ('FINALIZADA', 'FINALIZADA'), ('NÃO FINALIZADA', 'NÃO FINALIZADA')], max_length=100)),
                ('horainicial', models.DateTimeField(blank=True, null=True)),
                ('horafinal', models.DateTimeField(blank=True, null=True)),
                ('qnt_produzida', models.IntegerField(blank=True, null=True)),
                ('atributo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.atributo')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.empresa')),
                ('maquina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcp.maquinapcp')),
            ],
        ),
    ]
