from rest_framework import serializers
from bodegaApp.models import Adjunto

class AdjuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adjunto
        fields = '__all__'