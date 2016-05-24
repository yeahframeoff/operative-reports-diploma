from djoser.serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import DbConnection, Widget, Dashboard

User = get_user_model()


class UserSerializer(UserRegistrationSerializer):

    def validate_empty_values(self, data):
        data = data.copy()
        data['password'] = data['username']
        return super().validate_empty_values(data)


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
