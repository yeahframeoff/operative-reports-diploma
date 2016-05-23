from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import DBConnectionSerializer, WidgetConfigSerializer
from .models import DbConnection, DIAGRAM_TYPES, WidgetConfig


class DatabaseConnectionCreateAPIView(generics.ListCreateAPIView):
    serializer_class = DBConnectionSerializer
    queryset = DbConnection.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DatabaseConnectionAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DBConnectionSerializer
    queryset = DbConnection.objects.all()


class WidgetConfigCreateAPIView(generics.ListCreateAPIView):
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


@api_view(['GET'])
def get_db_schema(request, pk):
    db_conf = DbConnection.objects.get(pk=pk)
    return JsonResponse(db_conf.get_schema(), safe=False)


def _check_connection(db_conf):
    result = db_conf.check_connection()
    if result.success:
        return Response({'detail': "success"}, status=200)
    else:
        return Response({'detail': "fail",
                         "error": result.error_message},
                        status=400)


class CheckConnectionView(generics.GenericAPIView):

    serializer_class = DBConnectionSerializer
    queryset = DbConnection.objects.all()

    def get(self, request, *args, **kwargs):
        db_conf = self.get_object()
        return _check_connection(db_conf)


class CheckConnectionInstantView(generics.GenericAPIView):

    serializer_class = DBConnectionSerializer
    queryset = DbConnection.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        db_conf = DbConnection(**data)
        return _check_connection(db_conf)
