from django.http import JsonResponse
from django.contrib.auth import get_user_model

from rest_framework import generics as drf_generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .serializers import (
    DBConnectionSerializer,
    WidgetSerializer,
    DashboardSerializer,
    WidgetCreateSerializer,
    UserSerializer,
)
from .models import DbConnection, Widget, Dashboard, DIAGRAM_TYPES


class UserCreateAPIView(drf_generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.filter(is_superuser=False)
    permission_classes = IsAdminUser,


class UserAPIView(drf_generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.filter(is_superuser=False)
    permission_classes = IsAdminUser,


class DatabaseConnectionCreateAPIView(drf_generics.ListCreateAPIView):
    serializer_class = DBConnectionSerializer
    queryset = DbConnection.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DatabaseConnectionAPIView(drf_generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DBConnectionSerializer
    queryset = DbConnection.objects.all()


class DashboardCreateAPIView(drf_generics.ListCreateAPIView):
    serializer_class = DashboardSerializer
    queryset = Dashboard.objects.all()


class DashboardAPIView(drf_generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DashboardSerializer
    queryset = Dashboard.objects.all()


class WidgetListCreateAPIView(drf_generics.ListCreateAPIView):
    serializer_class = WidgetCreateSerializer
    lookup_field = 'dashboard_pk'

    def perform_create(self, serializer):
        serializer.save(dashboard_id=self.kwargs['dashboard_pk'])

    def get_queryset(self):
        if self.request.method == 'GET':
            return Widget.objects.filter(dashboard=self.kwargs['dashboard_pk'])
        else:
            return Widget.objects.all()


class WidgetAPIView(drf_generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WidgetSerializer
    queryset = Widget.objects.all()


@api_view(['GET'])
def get_types(request):
    return Response(dict(DIAGRAM_TYPES))


@api_view(['GET'])
def get_db_schema(request, pk):
    db_conf = drf_generics.get_object_or_404(DbConnection, pk=pk)
    return JsonResponse(db_conf.get_schema(), safe=False)


def _check_connection(db_conf):
    result = db_conf.check_connection()
    if result.success:
        return Response({'detail': "success"}, status=200)
    else:
        return Response({'detail': "fail",
                         "error": result.error_message},
                        status=400)


class CheckConnectionView(drf_generics.GenericAPIView):

    serializer_class = DBConnectionSerializer
    queryset = DbConnection.objects.all()

    def get(self, request, *args, **kwargs):
        db_conf = self.get_object()
        return _check_connection(db_conf)


class CheckConnectionInstantView(drf_generics.GenericAPIView):

    serializer_class = DBConnectionSerializer
    queryset = DbConnection.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        db_conf = DbConnection(**data)
        return _check_connection(db_conf)
