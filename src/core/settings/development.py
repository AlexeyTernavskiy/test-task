# -*- coding: utf-8 -*-

"""Development settings and globals."""

from .base import *

# DEBUG CONFIGURATION
DEBUG = True
# END DEBUG CONFIGURATION

# SECRET CONFIGURATION
# Note: This key should only be used for development and testing.
SECRET_KEY = 'um^n^*5u)&)pry%($+!2!&81&9481)&y85n$-pdoc(l4!k1)uo'
# END SECRET CONFIGURATION

# TEMPLATE CONFIGURATION
APP_DIRS = False
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': T_DIRS,
        'APP_DIRS': APP_DIRS,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': T_CONTEXT_PROCESSORS,
            'loaders': T_LOADERS,
        },
    },
]
# END TEMPLATE CONFIGURATION

# DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_database',
        'USER': 'vagrant',
        'PASSWORD': 'q!w@e3r4t%',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
# END DATABASE CONFIGURATION

# CACHE CONFIGURATION
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'debug-panel': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/debug-panel-cache',
        'OPTIONS': {
            'MAX_ENTRIES': 200
        }
    }
}
# END CACHE CONFIGURATION

# APP CONFIGURATION
INSTALLED_APPS += [
    'debug_toolbar',
    'debug_panel',
]
# END APP CONFIGURATION

# MIDDLEWARE CONFIGURATION
MIDDLEWARE_CLASSES += (
    'debug_panel.middleware.DebugPanelMiddleware',
)
# END MIDDLEWARE CONFIGURATION

# TOOLBAR CONFIGURATION
INTERNAL_IPS = ('127.0.0.1',)
# END TOOLBAR CONFIGURATION
