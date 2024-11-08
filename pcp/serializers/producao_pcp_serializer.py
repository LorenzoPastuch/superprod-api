from rest_framework import serializers
from pcp.models.producao_pcp import ProducaoPcp
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa
from cadastros.models.produto import Produto
from cadastros.models.molde import Molde
from pcp.models.maquina_pcp import MaquinaPcp
from pcp.models.insumos_pcp import InsumosPcp
from cadastros.models.atributo import Atributo
from cadastros.serializers.produto_serializer import ProdutoSerializer
from cadastros.serializers.atributo_serializer import AtributoSerializer
import math
from datetime import datetime, timedelta
import numpy as np
import pytz
from decimal import Decimal


class ProducaoPcpSerializer(serializers.ModelSerializer):
    atributo = serializers.SerializerMethodField()
    ciclo = serializers.SerializerMethodField()
    cavidades = serializers.SerializerMethodField()
    class Meta:
        model = ProducaoPcp
        fields = ['id', 'atributo', 'arte', 'quantidade', 'ordem', 'horainicial', 'horafinal', 'ciclo', 'cavidades', 'qnt_produzida', 'status', 'maquina']

    def create(self, validate_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        maquina = self.context['request'].data.get('maquina')
        atributo = self.context['request'].data.get('atributo', {}).get('id')
        arte = self.context['request'].data.get('arte')
        quantidade = self.context['request'].data.get('quantidade')
        status = self.context['request'].data.get('status')
        ordem = self.context['request'].data.get('ordem')
        horainicial = self.context['request'].data.get('horainicial')
        qnt_produzida = self.context['request'].data.get('qnt_produzida')

        produto = MaquinaPcp.objects.get(maquina=maquina).produto
        molde = Molde.objects.get(produto=produto.id)
        atributo = Atributo.objects.get(id=atributo)
        ciclo= molde.ciclo 
        cavidades= molde.cavidades

        if(horainicial):
            horas_necessarias = float(quantidade*ciclo/(3600*cavidades))
            horafinal = self.calcular_data_final(horainicial, horas_necessarias)
        else:
            horafinal = None 
            
        caixas = math.ceil(quantidade/produto.uncaixa)
        embalagens = math.ceil(quantidade/produto.unembalagem)

        if(produto.material == 'PS'):
            pigmento = Decimal(quantidade)*Decimal(0.02)*produto.peso
        else:
            if('TRANSLUCIDO' in atributo.nome or 'NEON' in atributo.nome):
                pigmento = Decimal(quantidade)*Decimal(0.03)*produto.peso
            else:
                pigmento = Decimal(quantidade)*Decimal(0.02)*produto.peso

        qnt_material = quantidade*produto.peso

        producao_pcp = ProducaoPcp.objects.create(
            maquina = MaquinaPcp.objects.get(id=maquina),
            atributo = atributo,
            arte=arte,
            quantidade = quantidade, 
            status = status,
            ordem = ordem,
            horainicial=horainicial,
            horafinal=horafinal,
            qnt_produzida=qnt_produzida,
            empresa=empresa_ativa
        )

        InsumosPcp.objects.create(
            producao = ProducaoPcp.objects.get(id=producao_pcp.id),
            caixas=caixas,
            pigmento=pigmento,
            embalagem=embalagens,
            qnt_material=qnt_material
        )

        return producao_pcp
    
    def update(self, instance, validate_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        maquina = self.context['request'].data.get('maquina', instance.maquina)
        atributo = self.context['request'].data.get('atributo', {}).get('id', instance.atributo.id)
        arte = self.context['request'].data.get('arte', instance.arte)
        quantidade = self.context['request'].data.get('quantidade', instance.quantidade)
        status = self.context['request'].data.get('status', instance.status)
        ordem = self.context['request'].data.get('ordem', instance.ordem)
        horainicial = self.context['request'].data.get('horainicial', instance.horainicial)
        qnt_produzida = self.context['request'].data.get('qnt_produzida', instance.qnt_produzida)

        produto = MaquinaPcp.objects.get(maquina=maquina).produto
        atributo = Atributo.objects.get(id=atributo)
        molde = Molde.objects.get(produto=produto.id)
        ciclo= molde.ciclo 
        cavidades= molde.cavidades

        if(horainicial):
            horas_necessarias = float(quantidade*ciclo/(3600*cavidades))
            horafinal = self.calcular_data_final(horainicial, horas_necessarias)
        else:
            horafinal = None 
        
        caixas = math.ceil(quantidade/produto.uncaixa)
        embalagens = math.ceil(quantidade/produto.unembalagem)

        if(produto.material == 'PS'):
            pigmento = Decimal(quantidade)*Decimal(0.02)*produto.peso
        else:
            if('TRANSLUCIDO' in atributo.nome or 'NEON' in atributo.nome):
                pigmento = Decimal(quantidade)*Decimal(0.03)*produto.peso
            else:
                pigmento = Decimal(quantidade)*Decimal(0.02)*produto.peso
        
        qnt_material = quantidade*produto.peso

        instance.empresa = empresa_ativa
        instance.maquina = MaquinaPcp.objects.get(id=maquina)
        instance.atributo = atributo
        instance.arte = arte
        instance.quantidade = quantidade
        instance.ordem = ordem
        instance.status = status
        instance.horainicial = horainicial
        instance.horafinal = horafinal
        instance.qnt_produzida = qnt_produzida

        instance.save()

        insumo = InsumosPcp.objects.get(producao=instance)
        insumo.caixas = caixas
        insumo.pigmento = pigmento
        insumo.embalagem = embalagens
        insumo.qnt_material = qnt_material

        insumo.save()

        return instance
 
    def get_atributo(self, obj):
        return AtributoSerializer(obj.atributo).data
    
    def calcular_data_final(self, hora_inicial, horas_necessarias):
        
        print(hora_inicial)
        hora_inicial = datetime.strptime(hora_inicial, "%Y-%m-%dT%H:%M:%S.%fZ")
        hora_inicial = hora_inicial - timedelta(hours=3) #soluçao podre pra resolver problema de fuso horario
        print(hora_inicial)

        inicio_dia_util = timedelta(hours=7)
        fim_dia_util = timedelta(hours=17)
        horas_por_dia = 10  
        # Configuração de horários e horas por dia útil
        hora_inicial_time = hora_inicial.time()
        if hora_inicial_time < (datetime.min + inicio_dia_util).time():
            hora_inicial = hora_inicial.replace(hour=7, minute=0, second=0)
        elif hora_inicial_time >= (datetime.min + fim_dia_util).time():
            hora_inicial = self.proximo_dia_util(hora_inicial + timedelta(days=1)).replace(hour=7, minute=0, second=0)

        # Passo 2: Divisão de dias e horas restantes
        dias_necessarios = int(horas_necessarias // horas_por_dia)
        horas_restantes = float(horas_necessarias % horas_por_dia)

        # Passo 3: Adição de dias completos de trabalho
        data_intermediaria = hora_inicial
        for _ in range(dias_necessarios):
            data_intermediaria = self.proximo_dia_util(data_intermediaria + timedelta(days=1))
        
        # Passo 4: Adição das horas restantes dentro do intervalo útil
        hora_final = data_intermediaria + timedelta(hours=horas_restantes)
        if hora_final.time() > (datetime.min + fim_dia_util).time():
            # Excedeu o expediente, ajusta para o próximo dia útil às 7:00
            excesso_horas = (hora_final - hora_final.replace(hour=17, minute=0, second=0)).seconds / 3600
            hora_final = self.proximo_dia_util(hora_final + timedelta(days=1)).replace(hour=7, minute=0, second=0)
            hora_final += timedelta(hours=excesso_horas)
        print(hora_final)
        return hora_final + timedelta(hours=3) #soluçao podre pra resolver problema de fuso horario

    def proximo_dia_util(self, data):
        # Move para o próximo dia útil, ignorando finais de semana
        while data.weekday() >= 5:  # 5 = sábado, 6 = domingo
            data += timedelta(days=1)
        return data

    def get_ciclo(self, obj):
        molde = Molde.objects.get(produto=obj.maquina.produto)
        ciclo= molde.ciclo 
        return ciclo
     
    def get_cavidades(self, obj):
        molde = Molde.objects.get(produto=obj.maquina.produto)
        cavidades= molde.cavidades
        return cavidades
    
