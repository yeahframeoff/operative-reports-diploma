import os

import psycopg2
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
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

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


@api_view(['GET'])
def get_db_schema(request, pk):
    db_conf = DbConnection.objects.get(pk=pk)
    connection = db_conf.conn
    cursor = connection.cursor()
    qqq = """
        SELECT table_name,
               COLUMN_NAME,
               udt_name as short_type_name,
               data_type as long_type_name,
               character_maximum_length as char_max_len
        FROM information_schema.columns
        WHERE table_catalog = '%s' and table_schema = 'public'
        ORDER BY ordinal_position;
    """ % db_conf.db_name
    # qqq = """\d foo"""
    cursor.execute(qqq)
    data = dictfetchall(cursor)
    connection.close()
    return JsonResponse(data, safe=False)


@api_view(['GET'])
def check_connection(request, pk):
    db_conf = DbConnection.objects.get(pk=pk)

    try:
        params = db_conf.conn.get_connection_params()
        conn = psycopg2.connect(**params)
        conn.close()
        return JsonResponse({'result': "success"}, status=200, safe=False)
    except Exception as e:
        error_message = str(e)
        return JsonResponse({'result': "fail", "error": error_message}, status=400, safe=False)


@api_view(['POST'])
def check_connection_instant(request):
    data = {
        'user': request.POST.get('user'),
        'password': request.POST.get('password'),
        'host': request.POST.get('host'),
        'port': int(request.POST.get('port')),
        'db_name': request.POST.get('db_name'),
    }
    db_conf = DbConnection(**data)

    try:
        params = db_conf.conn.get_connection_params()
        conn = psycopg2.connect(**params)
        conn.close()
        return JsonResponse({'result': "success"}, status=200, safe=False)
    except Exception as e:
        error_message = str(e)
        return JsonResponse({'result': "fail", "error": error_message}, status=400, safe=False)
