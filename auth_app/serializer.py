from rest_framework import serializers


class ValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=15)             # Username should be String with maximum characters 15
    password = serializers.CharField(max_length=15)             # Password should be String with maximum characters 15