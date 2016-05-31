from collections import namedtuple

from django.db import models
from django.db.utils import load_backend
from django.conf import settings


DIAGRAM_TYPES = [
    ('R', 'Round'),
    ('S', 'Stacked'),
    ('C', 'Curve'),
]


class DbConnection(models.Model):
    host = models.GenericIPAddressField()
    port = models.PositiveSmallIntegerField(null=False, default=5432)
    user = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    db_name = models.CharField(max_length=32)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    def get_config(self):
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': self.db_name,
            'USER': self.user,
            'PASSWORD': self.password,
            'HOST': self.host,
            'PORT': self.port,
            'TIME_ZONE': None,
            'CONN_MAX_AGE': 500,
            'AUTOCOMMIT': None,
            'OPTIONS': {}
        }

    @property
    def conn(self):
        db = self.get_config()
        backend = load_backend(db['ENGINE'])
        return backend.DatabaseWrapper(db, "remote postgres")

    CheckConnectionResult = namedtuple('CheckConnectionResult', ('success', 'error_message'))

    def check_connection(self):
        import psycopg2
        try:
            params = self.conn.get_connection_params()
            conn = psycopg2.connect(**params)
            conn.close()
            return self.CheckConnectionResult(True, None)
        except Exception as e:
            error_message = str(e)
            return self.CheckConnectionResult(False, error_message)

    def _dictfetchall(self, cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    def get_schema(self):
        query = """
            SELECT table_name,
                   COLUMN_NAME,
                   udt_name as short_type_name,
                   data_type as long_type_name,
                   character_maximum_length as char_max_len
            FROM information_schema.columns
            WHERE table_catalog = '%s' and table_schema = 'public'
            ORDER BY ordinal_position;
        """ % self.db_name
        data = self.run_query(query)
        grouped = {}

        for item in data:
            item_cp = dict((k, item[k]) for k in item if k != 'table_name')
            table_name = item['table_name']
            grouped.setdefault(table_name, []).append(item_cp)
        tables = [
            {
                'table_name': k,
                'columns': grouped[k]
            } for k in grouped
        ]

        return {'tables': tables}

    def run_query(self, query):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute(query)
        data = self._dictfetchall(cursor)
        conn.close()
        return data


class Dashboard(models.Model):
    name = models.CharField(max_length=32)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dashboards')


class Widget(models.Model):
    diagram_type = models.CharField(max_length=1, choices=DIAGRAM_TYPES)
    db_connection = models.ForeignKey(DbConnection)
    query = models.TextField()
    dashboard = models.ForeignKey(Dashboard)

    def display(self):
        return self.db_connection.run_query(self.query)
