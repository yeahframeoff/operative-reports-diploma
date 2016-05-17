import os

from django.db.utils import load_backend
from django.http import HttpResponse, JsonResponse


def hello(request):
    times = int(os.getenv('TIMES', 3))
    return HttpResponse('Hello! ' * times)


def db_info(request):

    user = os.getenv('TEST_DB_USERNAME')
    pwd = os.getenv('TEST_DB_PASSWORD')
    host = os.getenv('TEST_DB_HOST')
    port = os.getenv('TEST_DB_PORT')
    db_name = os.getenv('TEST_DB_NAME')
    db = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_name,
        'USER': user,
        'PASSWORD': pwd,
        'HOST': host,
        'PORT': port,
        'TIME_ZONE': None,
        'CONN_MAX_AGE': 500,
        'AUTOCOMMIT': None,
        'OPTIONS': {}
    }

    backend = load_backend(db['ENGINE'])
    conn = backend.DatabaseWrapper(db, "remote postgres")
    c = conn.cursor()
    c.execute('select * from a;')
    data = c.fetchall()
    conn.close()
    return JsonResponse({'data': data}, safe=False)
