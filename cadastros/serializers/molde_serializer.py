from rest_framework import serializers
from cadastros.models.molde import Molde


class MoldeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Molde
        fields = '__all__'

    
    
