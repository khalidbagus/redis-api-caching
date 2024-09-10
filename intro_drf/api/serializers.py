from rest_framework import serializers
from .models import *

class InstituionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institutions
        fields = '__all__'

class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = '__all__'

class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = '__all__'
