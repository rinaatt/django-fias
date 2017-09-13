from .settings import *

DATABASES['fias'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'fias_test',
    'USER': 'postgres',
    'PASSWORD': '',
    'HOST': '127.0.0.1',
    'PORT': '5432',
}

FIAS_DATABASE_ALIAS = 'fias'
DATABASE_ROUTERS = ['fias.routers.FIASRouter']

FIAS_SUGGEST_BACKEND = 'fias.suggest.backends.postgres_fts'

try:
    from .ext_db_pg_settings_local import *
except ImportError:
    print('Import Error')
    pass
