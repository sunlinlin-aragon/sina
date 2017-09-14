from django_settings import *
from url_settings import *

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'weibo',
        'USER': 'debian-sys-maint',
        'PASSWORD': 'EhmFvVG5lQyF0rVx',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
           'init_command': 'SET innodb_lock_wait_timeout = 120',
        },
    }
}


