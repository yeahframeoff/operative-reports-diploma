import ast
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

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='db_connections')

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
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dashboards')


class Widget(models.Model):
    diagram_type = models.CharField(max_length=1, choices=DIAGRAM_TYPES)
    db_connection = models.ForeignKey(DbConnection)
    query = models.TextField(null=True)
    columns = models.TextField(null=True)
    dashboard = models.ForeignKey(Dashboard, related_name='widgets')

    def run_query(self, query):
        return self.db_connection.run_query(query)

    def display_raw_query(self):
        return self.run_query(self.query)

    def display_structured_query(self):
        columns = ast.literal_eval(self.columns)
        query = self.make_query_from_columns(columns)
        return self.run_query(query)

    def display(self):
        if self.columns is not None:
            return self.display_structured_query()
        else:
            return self.display_raw_query()

    @staticmethod
    def make_query_from_columns(columns):
        tables = set(x[0] for x in columns)
        fields_str = ', '.join('"%s"."%s"' % tuple(x[:2]) for x in columns)
        tables_str = ', '.join(tables)
        return 'select %s from %s;' % (fields_str, tables_str)
