from rest_framework import serializers
from bodegaApp.models import Categoria  

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'