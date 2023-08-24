from rest_framework.serializers import ModelSerializer
from .models import DataEngCsv2

class TestDataSerializer(ModelSerializer):
    class Meta:
        model = DataEngCsv2
        fields = '__all__'