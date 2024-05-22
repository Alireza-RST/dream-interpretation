from rest_framework import serializers


class InterpretationSerializer(serializers.Serializer):
    content = serializers.CharField(required=True)