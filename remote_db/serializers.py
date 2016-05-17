from rest_framework import serializers
from .models import DbConnection, WidgetConfig


class DBConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbConnection
        fields = 'id', 'host', 'port', 'user', 'password', 'db_name'


class WidgetConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = WidgetConfig
        fields = 'id', 'diagram_type', 'query'
