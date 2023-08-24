from rest_framework.serializers import ModelSerializer
from .models import DataEngCsv3

class TestDataSerializer(ModelSerializer):
    class Meta:
        model = DataEngCsv3
        fields = '__all__'