from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def emitir_atualizacao_producao(instance):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "pcp_updates",
        {
            "type": "send_update",
            "data": instance.data
        }
    )
