# Generated by Django 5.1.1 on 2024-11-08 19:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razaosocial', models.CharField(max_length=255)),
                ('cnpj', models.CharField(max_length=14, unique=True)),
                ('cidade', models.CharField(max_length=100)),
                ('uf', models.CharField(max_length=2)),
                ('cep', models.CharField(max_length=8)),
                ('logradouro', models.CharField(max_length=255)),
                ('numero', models.CharField(max_length=10)),
                ('complemento', models.CharField(blank=True, max_length=100)),
                ('bairro', models.CharField(max_length=100)),
                ('nomecontato', models.CharField(blank=True, max_length=100)),
                ('telefone', models.CharField(blank=True, max_length=20)),
                ('whats', models.CharField(blank=True, max_length=20)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('status', models.BooleanField(default=True)),
                ('empresaativa', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Colaborador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('funcao', models.CharField(max_length=100)),
                ('numero', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Atributo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Maquina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('numero', models.IntegerField()),
                ('peso', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Molde',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('fabricante', models.TextField()),
                ('cavidades', models.IntegerField()),
                ('ciclo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='MoldeMaquina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maquina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.maquina')),
                ('molde', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.molde')),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('sku', models.CharField(max_length=100)),
                ('peso', models.DecimalField(decimal_places=3, max_digits=10)),
                ('material', models.CharField(choices=[('PS', 'Poliestireno'), ('PP', 'Polipropileno'), ('PEBD', 'Polietileno de Baixa Densidade'), ('TPE', 'Termoplastico Expandido')], max_length=100)),
                ('embalagem', models.CharField(max_length=10)),
                ('uncaixa', models.IntegerField()),
                ('unembalagem', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Producao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('horainicial', models.CharField(blank=True, max_length=100, null=True)),
                ('horafinal', models.CharField(blank=True, max_length=100, null=True)),
                ('quantidade', models.IntegerField()),
                ('perda', models.FloatField(null=True)),
                ('motivoperda', models.CharField(blank=True, max_length=100, null=True)),
                ('ciclo', models.FloatField(null=True)),
                ('lote', models.CharField(blank=True, max_length=100, null=True)),
                ('observacao', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('atributo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.atributo')),
                ('embalador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='embalador', to='cadastros.colaborador')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.empresa')),
                ('maquina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.maquina')),
                ('operador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operador', to='cadastros.colaborador')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.produto')),
            ],
        ),
        migrations.AddField(
            model_name='molde',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.produto'),
        ),
        migrations.CreateModel(
            name='Log_cadastro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comando', models.CharField(max_length=100)),
                ('datagravacao', models.DateTimeField()),
                ('usuariogravacao', models.CharField(max_length=100)),
                ('atributo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastros.atributo')),
                ('colaborador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastros.colaborador')),
                ('empresa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastros.empresa')),
                ('maquina', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastros.maquina')),
                ('molde', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastros.molde')),
                ('producao', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastros.producao')),
                ('produto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastros.produto')),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresapadrao', models.BooleanField(default=False)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.empresa')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
