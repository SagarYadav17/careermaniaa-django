from rest_framework import serializers


class CityMongoSerializer(serializers.Serializer):
    _id = serializers.CharField()
    id = serializers.CharField()
    state_name = serializers.CharField()
    name = serializers.CharField()
    district = serializers.CharField()
    division = serializers.CharField()
    pincode = serializers.CharField()
