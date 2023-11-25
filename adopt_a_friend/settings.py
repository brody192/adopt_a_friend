from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ko3&^p3c-^^41_c#r$#s-7q+_onf543=(676g#dx#ya0_@!sji'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['adoptafriend.up.railway.app', '127.0.0.1']
CSRF_TRUSTED_ORIGINS=['https://adoptafriend.up.railway.app']
CSRF_HEADER_NAME = "HTTP_X_CSRFTOKEN"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "verify_email.apps.VerifyEmailConfig",
    'main',
    'users',
    'videochat',
    'pets',
    'staff',
    'donation',
    'django_social_share',
    'chat',
    'testimonials',
    'reports'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'adopt_a_friend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'adopt_a_friend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'f3acBdeEbDcDEA4B25-GbD2EbC1f42a2',
        'HOST': 'monorail.proxy.rlwy.net',
        'PORT': '13486',
    }
}

# # settings.py

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'railway',
#         'USER': 'root',
#         'PASSWORD': 'adFaGFabeec-5FB16AfeBbC65dAh2bbc',
#         'HOST': 'roundhouse.proxy.rlwy.net',    # Set to the MySQL server's hostname or IP address
#         'PORT': '18063',         # MySQL default port is 3306
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'nhoryybanez13@gmail.com'
EMAIL_HOST_PASSWORD = 'bxle vypt xmmd moyx'

DEFAULT_FROM_EMAIL = 'noreply<no_reply@domain.com>'

AUTH_USER_MODEL = 'users.Users'

LOGOUT_REDIRECT_URL = '/login/'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache",
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MAX_RETRIES = 6

# HTML_MESSAGE_TEMPLATE = "users/email.html"

#VERIFICATION_SUCCESS_TEMPLATE = "users/new_email.html"

#VERIFICATION_FAILED_TEMPLATE = "path/to/failed.html"

REQUEST_NEW_EMAIL_TEMPLATE = "users/request_new_email.html"

#LINK_EXPIRED_TEMPLATE = 'path/to/expired.html'

#NEW_EMAIL_SENT_TEMPLATE  = 'users/new_email.html'

LOGIN_URL = "login"

DEFAULT_FILE_STORAGE = "storages.backends.s3.S3Storage"
AWS_ACCESS_KEY_ID = 'AKIA6GLHW6R2RWDQQNFU'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'adopt-a-friend'
AWS_S3_REGION_NAME = 'ap-southeast-2'
AWS_QUERYSTRING_EXPIRE = 600
AWS_S3_CUSTOM_DOMAIN = "d2jao7siktrha4.cloudfront.net"
AWS_CLOUDFRONT_KEY_ID='KPQU4NDZ0YWX1'
AWS_CLOUDFRONT_KEY='-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEApHvAzduBIvyyouV9d5ZuyncfohPO0HqonrHP8Txx3WaEReRu\nLqx1wHusgTAIdyHphaACb8Y41wn1ThShd239vpoCbGxvOzCbC6EqSQiui+DZTiVw\nrzKG3RmEtTV0NXZYs9h+jen3APwSD9U9YAZoXyyjeTSWsAc6GVKY11Jt7ckcyFu+\n87ca4OCLwhiIn3rfgf+Hm1NMk5RYVfVuci+PDaDKRnznfncftgwU4Qo9N9eP9OGA\nC7uIlRTazVXu4lVnV3aTZC+CrKg92X6FV/PAavQ+9vmUrLrcWBfPAWPsoTtzADwU\nSyRA5iVrDhSCCz1+5lOV1aYuZdkE1if7aahfpwIDAQABAoIBAH4H9OvHTWOpjJcU\nkNaZBbtNG4fs9YL4+UrfpB2L2xNyAdgr9+D7dB5QpRU34MSnz2778+IBWHwsvTFe\nzXndZZguGb1KONB5pdN7YhMj+9piJx+hwH39kSjI7M6MbsaoL79eG1pR81lly9El\n6ykwv7htU7UDfpLSdsoAZ+xU1LZlL1ld8GhsNg8eC3D1/DX3TnkYpyaL/tZK01uW\n7Dqdxczf8Tkr7Wz8c20xMS2DSPxhlItLV0Qu1MVOlqplRJ6n2yLqFa4ADjMUpLpp\nbRDphwJj0yfqUl8QWjpq/Ka1PM2mqQH7qVmI+/aZDghE+CvQ8VYSZ6K25FKk5E/g\nUF4m1AECgYEA4FYUNPFYORsEXHKeLHJm82bCj22z72SaQvdsifG1CTtmBQoTGx4h\n2lzxBggcC33jcpUeOr+3AiKmo2VoFcj/f36Brvv1/H5+a5D8SxAnvBMOM2Ct22q7\n8INxbKILri7IT2JoCY+6PpdB6s/SS0FoQzpklHEVPSFrR/+SVz7FJGcCgYEAu7ME\nZl9f/absz8JRYwHzjt9fOgHi3+JLesQTJpBVU2YfiVwTd1ZfTTYCENo2eIdeWhOJ\n1YLMz0QKzleDkgiXZTPrLsFuMgb/FLmSItFeL8IV0MxtxDi5VmJ4LlLa8CsPeGcd\nByhLg/ZH2KffmLTS12OlR62To5tqEoqfGhTT4sECgYBTeJPiMx7ReLUBtQAXp6WY\n0VZ5SadW3sbrPebb2Ny0h65pF5uOToLoHgbsaJ4OxJOZsdRipazxlXUNfRDicjxm\n8upL8qJPhb2CRpspTuSJ/UkeYs2tw6QUVMQiWJUiBXQw3Xu6ewkgeuVi+lrT941U\n3mhIN19gtIuXaYfJAKkX5wKBgEbBcBorP+M9hq224blB5g9ostwKE/0zsCJiQZna\n9N9Qcvjzxb7Jx3kyr8qsh7YdyXqJPP9IpG5Jhw1LviRRqsiSrshcUG75ZjTo02be\np/O25URlm8dJXsxqqEVGJJQ+l0FbFX06OmVPdLv+ZHKLT6O0Q3zmuO4GyxCcQuex\nDELBAoGAOYEGjIMF9vKCOE0wYAO/V+e7iSzUUB89ZuKGzp1MS3hV39OosERbRkM1\nbO8x1DCahG826TKovzVwtIRaRKToxNMFZNCwXFAnDuj9CLhfhsOvmfDyaqyKj/lC\nejkhXHjuLgrS/kgGUdtT2mGPiWEBl95lKm9qByFA4pqi1yOpj4s=\n-----END RSA PRIVATE KEY-----'
