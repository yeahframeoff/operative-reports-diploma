from rest_framework import serializers
from .models import DbConnection


class DBConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbConnection
        fields = ['host', 'port', 'user', 'password', 'db_name']

    def validate_owner(self, value):
        return self.context['request'].user
