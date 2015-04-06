# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't03-&np((8a_9%fegm2qrulo!ulok&2drn2b%s6d8%ll4+@j9q'

# SECURITY WARNING: don't run with debug turned on in production!


DEBUG = True

TEMPLATE_DEBUG = True

#ALLOWED_HOSTS = ['104.236.0.177']
ALLOWED_HOSTS = ['*']

ADMINS = (
     ('Gabriel Romero', 'galexanderomero24@gmail.com'),
)

MANAGERS = ADMINS
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hidro_core',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hidro_sys.urls'

WSGI_APPLICATION = 'hidro_sys.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'hidro_sysdb',
        'USER': 'root',
        'PASSWORD': 'pegazo13',
        'HOST': '104.236.0.177',   # Or an IP Address that your DB is hosted on
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
TIME_ZONE = 'America/Guayaquil'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-EC'

#LANGUAGE_CODE = 'en-us'
#TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'galexanderomero24@gmail.com'
EMAIL_HOST_PASSWORD = '*******'
EMAIL_USE_TLS = True
