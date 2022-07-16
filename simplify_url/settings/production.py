import dj_database_url

from simplify_url.settings.common import *

DEBUG = False

ALLOWED_HOSTS = ['0.0.0.0', os.environ.get('PRODUCTION_HOST')]
CSRF_TRUSTED_ORIGINS = ["https://"+str(os.environ.get("PRODUCTION_HOST"))]

INSTALLED_APPS.extend(["whitenoise.runserver_nostatic"])

# Must insert after SecurityMiddleware, which is first in settings/common.py
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATICFILES_DIRS = ['simplify_app/static']
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_URL = "/static/"

DATABASE_URL = os.environ.get('DATABASE_URL')
db_from_env = dj_database_url.config(
    default=DATABASE_URL, conn_max_age=500, ssl_require=True)
DATABASES['default'].update(db_from_env)
