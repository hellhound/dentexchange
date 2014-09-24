# -*- coding:utf-8 -*-
'''
Django settings for Dentexchange project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
'''
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.realpath(os.path.dirname(__file__))
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

# Apps path
sys.path.insert(0, os.path.join(ROOT_DIR, 'apps'))

# Site ID

SITE_ID = 1

INTERNAL_IPS = (
    '127.0.0.1',
    '::1',
)

DOMAIN_NAME = 'dentexchange.com'

ALLOWED_HOSTS = (
    '.%s' % DOMAIN_NAME,
    '.%s.' % DOMAIN_NAME,
    '127.0.0.1',
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sg7a1r@fdzsw6!zo*am2t*e4a0n8xxi*a$q6ok!)vz6g_s=r2y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
)

INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.messages',
)

INSTALLED_APPS += (
    'south',
    'bootstrap3',
    'tinymce',
    'djcelery',
    'bootstrap_pagination',
    'robots',
    'haystack',
    'celery_haystack',
    'debug_toolbar',
    'haystack_panel',
    'feedback',
    'ajax_upload',
    'django_extensions',
)

INSTALLED_APPS += (
    'base',
    'contact',
    'location',
    'authentication',
    'registration',
    'home',
    'employer',
    'employee',
    'membership',
    'search',
    'matches',
)

INSTALLED_APPS += (
    'autofixtures',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.debug',
    'django.contrib.messages.context_processors.messages',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'libs.context_processors.conf',
    'libs.context_processors.debug',
)

TEMPLATE_DIRS = (
    os.path.realpath(os.path.join(ROOT_DIR, 'templates')),

)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dentexchange',
        'USERNAME': 'dentexchange',
        'HOST': '/var/run/postgresql'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.realpath(os.path.join(ROOT_DIR, 'static'))
MEDIA_ROOT = os.path.realpath(os.path.join(ROOT_DIR, 'media'))


AUTHENTICATION_BACKENDS = (
    'libs.auth.backends.ModelEmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)


LOGIN_URL = '/registration/'
LOGIN_REDIRECT_URL = '/'


CONTEXT_CONF = dict(
    # CDNs
    CDN_JQUERY_VERSION='2.1.1',
    CDN_JQUERYUI_VERSION='1.10.4',
    CDN_JSRENDER_VERSION='1.0pre35',
    CDN_HOLDER_VERSION='2.3.2',
    CDN_FONT_AWESOME_VERSION='4.1.0',
    CDN_CHOSEN_VERSION='1.1.0',
    CDN_SPINJS_VERSION='2.0.1',
    # Stripe
    STRIPE_PUBLISHABLE_KEY='',
)

# Stripe

STRIPE_SECRET_KEY=''

# Celery

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
BROKER_URL = 'amqp://guest:guest@localhost:5672'
CELERY_TIMEZONE = 'UTC'
import djcelery
djcelery.setup_loader()

# Admin tools

ADMIN_TOOLS_THEMING_CSS = 'base/css/admin-theming.css'
ADMIN_TOOLS_INDEX_DASHBOARD = {
    'libs.admin.site': 'dashboard.CustomIndexDashboard',
}

# SendGrid

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'dentexchange'
EMAIL_HOST_PASSWORD = ''

# Robots

ROBOTS_CACHE_TIMEOUT = 60 * 60 * 24 # 24 hours

# Debug Toolbar

DEBUG_TOOLBAR_PATCH_SETTINGS = False

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
)

DEBUG_TOOLBAR_PANELS += (
    'haystack_panel.panel.HaystackDebugPanel',
)

# Haystack

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/dentexchange'
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'

try:
    from local_settings import *
except ImportError:
    pass
