import os
from datetime import datetime
current_year = datetime.now().year
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hm6=$f461z&e)ke^w89p#(lgv0&=x5gq&l!$yey#)qw)ou!+#g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'projektmgr.com', 'www.projektmgr.com']


# Application definition
DBBACKUP_FILESYSTEM_DIRECTORY = os.path.join(BASE_DIR, 'dbbackup')
INSTALLED_APPS = [
    #'app_system',
    
    'app_analytics',
    'app_jivapms',
    'app_memberprofilerole',
    'app_organization',
    'app_loginsystem',
    'app_common',
    'app_web',
    'app_org_blog',
    'app_scrum_product',
    'app_scrum',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    

    'app_web.templatetags',
    'mptt',
    'crispy_forms',
    'crispy_bootstrap5',
    'markdownx',
    'markdown',    
    'imagekit',
    'app_user',
    'apps.app_usermgmt',
    'apps.app_todos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app_analytics.middleware.page_visit_middleware.PageAnalyticsMiddleware',
]

ROOT_URLCONF = 'project_mgr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app_web.context_processors.settings_context_processor.get_site_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'project_mgr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'
TIME_ZONE = 'Asia/Kolkata'
LOGIN_URL = '/loginsystem/login/'

#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
#DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# Step3: added the context processors in the app_web/context_processors/settings_context_processors.py


### Logging
# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'INFO',  # Set level based on DEBUG
    },
}
### End logging

## CUSTOMIZATION
BUILD_VERSION = 'test_1.0.0'
BUILD_DESCRIPTION = 'preparing the tree_one_crud_advanced'
## TEMPLATE DISPLAY
SITE_TITLE = "Jiva PMS"
CODING_AI = "codingagi1"
SITE_NAME = f"{SITE_TITLE}"
CONTACT_EMAIL = "contact@a{SITE_TITLE}.com"
## copyright information
PRIVACY_INFO = "No Privacy Information collected and utilized. Jiva Project Management System."
COPYRIGHT_INFO = f"© {current_year}. {PRIVACY_INFO} All rights reserved."

SITE_CAPTION = f"{SITE_TITLE} an open-source project management system aimed at startups and enterprises."

SITE_DESC = f"""
{SITE_TITLE} is a Project Management System for individuals, teams, enterprises and startups.
"""
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

"""
Log Levels:
DEBUG: Detailed information, typically of interest only when diagnosing problems.
INFO: Confirmation that things are working as expected.
WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g., ‘disk space low’). The software is still working as expected.
ERROR: Due to a more serious problem, the software has not been able to perform some function.
CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
"""


import environ
import os

# Define the path to the .env file
ENV_PATH = os.path.abspath("../../../../../../../.dev-env")  # Ensure the absolute path

# Initialize environment variables
env = environ.Env()

# Check if the file exists before reading it
if os.path.exists(ENV_PATH):
    environ.Env.read_env(env_file=ENV_PATH)  # Specify the file path
    #print(f"Environment file found: {ENV_PATH}")  # Debugging statement
else:
    print(f"Environment file NOT found at {ENV_PATH}")  # Debugging statement

# Check if environment variables are loaded correctly
try:
    EMAIL_HOST_USER = env("EMAIL_ADDR_NAME")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    #print(f"EMAIL_HOST_USER loaded: {EMAIL_HOST_USER}")  # Debugging statement
except environ.ImproperlyConfigured as e:
    print(f"Error loading environment variables: {e}")  # Debugging statement

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
