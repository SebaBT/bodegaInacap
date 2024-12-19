from rest_framework import serializers
from bodegaApp.models import Caja  

class CajaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caja
        fields = '__all__'