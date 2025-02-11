DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ALLOWED_HOSTS = [
    "example.com",
]

INSTALLED_APPS = [
    "django.contrib.sites",
    "regex_redirects",
]

SECRET_KEY = "notimportant"

APPEND_SLASH = False

MIDDLEWARE = ["regex_redirects.middleware.RedirectFallbackMiddleware"]

SITE_ID = 1

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django seems to require a ROOT_URLCONF.
ROOT_URLCONF = __name__
urlpatterns = []
