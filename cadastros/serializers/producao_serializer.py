from rest_framework import serializers
from cadastros.models.producao import Producao
from cadastros.models.usuario import Perfil
from cadastros.models.empresa import Empresa
from cadastros.models.colaborador import Colaborador
from cadastros.models.produto import Produto
from cadastros.models.maquina import Maquina
from cadastros.models.atributo import Atributo
from cadastros.serializers.atributo_serializer import AtributoSerializer
from cadastros.serializers.colaborador_serializer import ColaboradorSerializer
from cadastros.serializers.maquina_serializer import MaquinaSerializer
from cadastros.serializers.produto_serializer import ProdutoSerializer
from cadastros.serializers.log_cadastro_serializer import LogCadastroMixin
from cadastros.models.log_cadastro import Log_cadastro

class ProducaoSerializer(LogCadastroMixin, serializers.ModelSerializer):
    operador = serializers.SerializerMethodField()
    embalador = serializers.SerializerMethodField()
    produto = serializers.SerializerMethodField()
    maquina = serializers.SerializerMethodField()
    atributo = serializers.SerializerMethodField()
    usuariogravacao = serializers.SerializerMethodField()
    datagravacao = serializers.SerializerMethodField()

    class Meta:
        model = Producao
        fields = ['id', 'data', 'horainicial', 'horafinal', 'operador', 'embalador', 'produto', 'maquina', 'quantidade', 'atributo', 'perda', 'motivoperda', 'ciclo', 'lote', 'observacao', 'status', 'usuariogravacao', 'datagravacao']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        data = self.context['request'].data.get('data')
        operador = self.context['request'].data.get('operador', {})
        embalador = self.context['request'].data.get('embalador', {})
        produto = self.context['request'].data.get('produto', {})
        maquina = self.context['request'].data.get('maquina', {})
        atributo = self.context['request'].data.get('atributo', {})
        quantidade = self.context['request'].data.get('quantidade')
        horainicial = self.context['request'].data.get('horainicial')
        horafinal = self.context['request'].data.get('horafinal')
        perda = self.context['request'].data.get('perda')
        motivoperda = self.context['request'].data.get('motivoperda')
        ciclo = self.context['request'].data.get('ciclo')
        lote = self.context['request'].data.get('lote')
        observacao = self.context['request'].data.get('observacao')
        status = self.context['request'].data.get('status')
        

        producao = Producao.objects.create(
            empresa=empresa_ativa,
            operador = Colaborador.objects.get(id=operador['id']),
            embalador = Colaborador.objects.get(id=embalador['id']),
            produto = Produto.objects.get(id=produto['id']),
            maquina = Maquina.objects.get(id=maquina['id']),  
            atributo = Atributo.objects.get(id=atributo['id']),
            quantidade = quantidade,
            data = data,
            horainicial = horainicial,
            horafinal = horafinal,
            perda = perda,
            motivoperda = motivoperda,
            ciclo = ciclo,
            lote = lote,
            observacao = observacao,
            status = status,
        )

        self.registrar_log(
            comando=f"Criar Produção de ID {producao.id}",
            usuario=user,
            instance=producao,
        )
        return producao
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user

        perfil = Perfil.objects.get(usuario=user)
        id_empresa_ativa = perfil.empresaativa
        empresa_ativa = Empresa.objects.get(id=id_empresa_ativa)

        data = self.context['request'].data.get('data', instance.data)
        operador = self.context['request'].data.get('operador', {}).get('id', instance.operador.id)
        embalador = self.context['request'].data.get('embalador', {}).get('id', instance.embalador.id)
        produto = self.context['request'].data.get('produto', {}).get('id', instance.produto.id)
        maquina = self.context['request'].data.get('maquina', {}).get('id', instance.maquina.id)
        atributo = self.context['request'].data.get('atributo', {}).get('id', instance.atributo.id)
        quantidade = self.context['request'].data.get('quantidade', instance.quantidade)
        horainicial = self.context['request'].data.get('horainicial', instance.horainicial)
        horafinal = self.context['request'].data.get('horafinal', instance.horafinal)
        perda = self.context['request'].data.get('perda', instance.perda)
        motivoperda = self.context['request'].data.get('motivoperda', instance.motivoperda)
        ciclo = self.context['request'].data.get('ciclo', instance.ciclo)
        lote = self.context['request'].data.get('lote', instance.lote)
        observacao = self.context['request'].data.get('observacao', instance.observacao)
        status = self.context['request'].data.get('status', instance.status)

        # Atualiza os campos do objeto 'instance'
        instance.empresa = empresa_ativa
        instance.operador = Colaborador.objects.get(id=operador)
        instance.embalador = Colaborador.objects.get(id=embalador)
        instance.produto = Produto.objects.get(id=produto)
        instance.maquina = Maquina.objects.get(id=maquina)
        instance.atributo = Atributo.objects.get(id=atributo)
        instance.quantidade = quantidade
        instance.data = data
        instance.horainicial = horainicial
        instance.horafinal = horafinal
        instance.perda = perda
        instance.motivoperda = motivoperda
        instance.ciclo = ciclo
        instance.lote = lote
        instance.observacao = observacao
        instance.status = status

        instance.save()

        self.registrar_log(
            comando=f"Atualizar Produção de ID {instance.id}",
            usuario=user,
            instance=instance,
        )
        return instance

    def get_operador(self, obj):
        return ColaboradorSerializer(obj.operador).data
    
    def get_embalador(self, obj):
        return ColaboradorSerializer(obj.embalador).data
    
    def get_produto(self, obj):
        return ProdutoSerializer(obj.produto).data
    
    def get_maquina(self, obj):
        return MaquinaSerializer(obj.maquina).data
    
    def get_atributo(self, obj):
        return AtributoSerializer(obj.atributo).data
    
    def get_usuariogravacao(self, obj):
        # Busca o log mais recente relacionado ao atributo
        log = Log_cadastro.objects.filter(producao=obj).order_by('-datagravacao').first()
        if log:
            return log.usuariogravacao
        return None

    def get_datagravacao(self, obj):
        # Busca o log mais recente relacionado ao atributo
        log = Log_cadastro.objects.filter(producao=obj).order_by('-datagravacao').first()
        if log:
            return log.datagravacao
        return None