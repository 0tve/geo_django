from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from django.contrib.auth import models as auth_models

from . import models


class PointSerializer(gis_serializers.GeoFeatureModelSerializer):
    class Meta:
        model = models.Point
        geo_field = 'location'
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = ['id', 'text']


class GeoParamsSerializer(serializers.Serializer):
    latitude = serializers.FloatField(min_value=-90, max_value=90)
    longitude = serializers.FloatField(min_value=-180, max_value=180)
    radius = serializers.FloatField(min_value=0.001)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = auth_models.User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        return auth_models.User.objects.create_user(**validated_data)
