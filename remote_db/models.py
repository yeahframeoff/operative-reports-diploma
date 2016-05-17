from django.conf import settings
from django.db import models
from django.db.utils import load_backend


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
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
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
