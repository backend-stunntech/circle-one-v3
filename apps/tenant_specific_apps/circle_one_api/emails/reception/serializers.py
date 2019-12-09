from rest_framework import serializers


class SnsMessageSerializer(serializers.Serializer):
    Message = serializers.JSONField()
