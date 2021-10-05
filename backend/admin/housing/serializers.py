from rest_framework import serializers
from .models import Housing as housing

class HousingSerializer(serializers.Serializer):
    id = serializers.CharField()
    latitude = serializers.FloatField()
    housing_median_age = serializers.FloatField()
    total_rooms = serializers.FloatField()
    total_bedrooms = serializers.FloatField()
    population = serializers.FloatField()
    households = serializers.FloatField()
    median_income = serializers.FloatField()
    median_house_value = serializers.FloatField()
    ocean_proximity = serializers.CharField()

    class Meta:
        model = housing
        fields = '__all__'

    def create(self, validated_data):
        return housing.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return housing.objects.filter(pk=instance.housing_id).update(**validated_data)