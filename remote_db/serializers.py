from rest_framework import serializers
from .models import DbConnection, Widget, Dashboard


class DBConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbConnection
        fields = 'id', 'host', 'port', 'user', 'password', 'db_name'


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = 'id', 'name'


class WidgetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = 'id', 'diagram_type', 'query'


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = 'id', 'diagram_type', 'query', 'dashboard'
