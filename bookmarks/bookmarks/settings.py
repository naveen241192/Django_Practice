"""
Django settings for bookmarks project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q#5%ed$$=&a68w#=*i6^6ew4#%e&=qrre_j-wsyma7-kel%6)i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['mysite.com', 'localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'django.contrib.admin',  # this should be after account, bcoz both templates are in same relative path, loads the 1st one it finds.
    #'social.apps.django_app.default',  # to support social app authentication.
    #'social_auth',
    'social_django',
    'images',
    'sorl.thumbnail',  # for creating thumbnails to images.
    'actions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'bookmarks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect', # <--
            ],
        },
    },
]

WSGI_APPLICATION = 'bookmarks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# for django to support media files
MEDIA_URL = '/media/'                          # base url to serve the media files uloaded by the users.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')  # local path where they reside

# indicates the class to use to send emails,
# EmailBackend allows to write emails to console.
# (yo can see email on ur console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'naveen.bijjala33@gmail.com'
EMAIL_HOST_PASSWORD = 'flareon1'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


from django.core.urlresolvers import reverse_lazy

LOGIN_REDIRECT_URL = reverse_lazy('dashboard')   # tells django to redirect to this page after login. if there is no next parameter.
# to redirect to login
LOGIN_URL = reverse_lazy('login') # reverse_lazy is same as reverse, builds the url dynamically by their name.
# to redirect to logout
LOGOUT_URL = reverse_lazy('logout')

# python-social-auth settings
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',

    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
)
SOCIAL_AUTH_GOOGLE_OAUTH2_USE_DEPRECATED_API = True
SOCIAL_AUTH_GOOGLE_PLUS_USE_DEPRECATED_API = True

SOCIAL_AUTH_FACEBOOK_KEY = '233313390510522'
SOCIAL_AUTH_FACEBOOK_SECRET = '35cbe6afa6f0100e19d83519e39c97b2'

SOCIAL_AUTH_TWITTER_KEY = 'kK66CnsawdeyflwbAEus98YxI'
SOCIAL_AUTH_TWITTER_SECRET = 'p0UrT8LsO7lCT1hajsn8ge2PCoC7B0XeLUyUk57ZLWqqdG2arV'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '313681665843-c9nh17kljdo5qtpnt8lv13u6qvmmf883.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'MHkJTbuqnJDE_ihCqIBMXVqM'


# django adds a get_absolute_url_method dynamically to any model that appears in ABSOLUTE_URL_OVERRIDES setting.
# this method returns the corresponding setting for the given model specified in the setting.

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('user_detail', args=[u.username])
}


# Redis Server Configuration
"""

We are using Redis here for storing views (like no of persons viewed this image), 
bcoz if we use update queries they would be very complex
and decreases performance, hence we use redis to store Item Views.

"""
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
