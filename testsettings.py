from django.conf import global_settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.sites',
    'regex_redirects',
]

SECRET_KEY = "notimportant"

APPEND_SLASH = False

# Using MIDDLEWARE_CLASSES
# MIDDLEWARE_CLASSES = list(global_settings.MIDDLEWARE_CLASSES) + \
#                      ['regex_redirects.middleware.RedirectFallbackMiddleware']

SITE_ID = 1

# Django seems to require a ROOT_URLCONF.
ROOT_URLCONF = __name__
urlpatterns = []
