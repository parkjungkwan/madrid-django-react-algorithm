from rest_framework import serializers
# pip install Django django-rest-framework
from .models import Member as user

class MemberSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    name = serializers.CharField()
    email = serializers.CharField()
    birth = serializers.CharField()
    address = serializers.CharField()
    class Meta:
        model = user
        fileds = '__all__'

    def create(self, valided_data):
        return user.objects.create(**valided_data)

    def update(self, instance, valided_data):
        user.objects.filter(pk=instance.username).update(**valided_data)
