import dj_database_url
import environ

env = environ.Env()

# DATABASES = {
#     'default': dj_database_url.config(
#         default='postgres://{0}:{1}@{2}:{3}/{4}'.format(
#             env("DJANGO_POSTGRES_USER", default='admin'),
#             env("DJANGO_POSTGRES_PASSWORD", default='password'),
#             env("DJANGO_POSTGRES_HOST", default='postgres'),
#             env("DJANGO_POSTGRES_PORT", default='5432'),
#             env("DJANGO_POSTGRES_DB", default='crm_db')), ),
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgresql',
        'USER': 'postgres',
        'PASSWORD': 'Predator1861!',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASE_ROUTERS = ['settings.dbrouters.DbRouter', ]
