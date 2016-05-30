from djoser.serializers import UserRegistrationSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import DbConnection, Widget, Dashboard

User = get_user_model()


class UserCreateSerializer(UserRegistrationSerializer):

    dashboards = serializers.PrimaryKeyRelatedField(many=True, queryset=Dashboard.objects.all())

    class Meta(UserRegistrationSerializer.Meta):
        fields = list(UserRegistrationSerializer.Meta.fields) + ['dashboards']

    def validate_empty_values(self, data):
        data = data.copy()
        data['password'] = data['username']
        return super().validate_empty_values(data)

    def create(self, validated_data):
        dashboards = validated_data['dashboards']
        del validated_data['dashboards']
        user = super().create(validated_data)
        user.dashboards.set(dashboards)
        return user


class UserShowSerializer(UserSerializer):
    role = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = list(UserSerializer.Meta.fields) + ['role']

    def get_role(self, obj):
        return 'admin' if obj.is_superuser else 'user'


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
