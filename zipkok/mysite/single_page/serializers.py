from rest_framework.serializers import ModelSerializer
from .models import DataEngCsv

class TestDataSerializer(ModelSerializer):
    class Meta:
        model = DataEngCsv
        fields = '__all__'