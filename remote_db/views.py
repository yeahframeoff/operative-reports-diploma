from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import DBConnectionSerializer
from .models import DbConnection, DIAGRAM_TYPES


class DatabaseConnectionCreateAPIView(generics.CreateAPIView):
    serializer_class = DBConnectionSerializer
    queryset = DbConnection.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DatabaseConnectionAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DBConnectionSerializer
    queryset = DbConnection.objects.all()


@api_view(['GET'])
def get_types(request):
    return Response(DIAGRAM_TYPES)
