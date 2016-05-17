from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import DBConnectionSerializer, WidgetConfigSerializer
from .models import DbConnection, DIAGRAM_TYPES, WidgetConfig


class DatabaseConnectionCreateAPIView(generics.CreateAPIView):
    serializer_class = DBConnectionSerializer
    queryset = DbConnection.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DatabaseConnectionAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DBConnectionSerializer
    queryset = DbConnection.objects.all()


class WidgetConfigCreateAPIView(generics.CreateAPIView):
    serializer_class = WidgetConfigSerializer
    queryset = WidgetConfig.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WidgetConfigAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WidgetConfigSerializer
    queryset = WidgetConfig.objects.all()


@api_view(['GET'])
def get_types(request):
    return Response(dict(DIAGRAM_TYPES))
