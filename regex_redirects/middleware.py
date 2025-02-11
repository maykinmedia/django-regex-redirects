import logging
import re

from django import http
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.db.models.expressions import F

from .models import Redirect

logger = logging.getLogger(__name__)


try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object  # fallback for Django < 1.10

DJANGO_REGEX_REDIRECTS_CACHE_KEY = "django-regex-redirects-regular"
DJANGO_REGEX_REDIRECTS_CACHE_REGEX_KEY = "django-regex-redirects-regex"
DJANGO_REGEX_REDIRECTS_CACHE_TIMEOUT = 60

"""
A modified version of django.contrib.redirects, this app allows
us to optionally redirect users using regular expressions.

It is based on: http://djangosnippets.org/snippets/2784/
"""


class RedirectFallbackMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        if "django.contrib.sites" not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured(
                "You cannot use RedirectFallbackMiddleware when "
                "django.contrib.sites is not installed."
            )
        super(RedirectFallbackMiddleware, self).__init__(*args, **kwargs)

    def increment_redirect(self, pk):
        def increment():
            try:
                Redirect.objects.filter(pk=pk).update(
                    nr_times_visited=F("nr_times_visited") + 1
                )
            except Exception:
                logger.warning("Increment nr_times_visited failed.")
                raise

        # https://docs.djangoproject.com/en/5.1/topics/db/transactions/#performing-actions-after-commit
        # All errors derived from Python’s Exception class are caught and logged to the
        # django.db.backends.base logger.
        transaction.on_commit(increment)

    def process_response(self, request, response):
        if response.status_code != 404:
            return response  # No need to check for a redirect for non-404 responses.

        full_path = request.get_full_path()
        http_host = request.META.get("HTTP_HOST", "")
        if http_host:
            if request.is_secure():
                http_host = "https://" + http_host
            else:
                http_host = "http://" + http_host

        redirects = cache.get(DJANGO_REGEX_REDIRECTS_CACHE_KEY)
        if redirects is None:
            redirects = list(
                Redirect.objects.all().order_by("fallback_redirect").values()
            )
            cache.set(
                DJANGO_REGEX_REDIRECTS_CACHE_KEY,
                redirects,
                DJANGO_REGEX_REDIRECTS_CACHE_TIMEOUT,
            )

        for redirect in redirects:
            # Attempt a regular match
            if redirect["old_path"] == full_path:
                self.increment_redirect(redirect["id"])
                if redirect["new_path"].startswith("http"):
                    return http.HttpResponsePermanentRedirect(redirect["new_path"])
                else:
                    return http.HttpResponsePermanentRedirect(
                        http_host + redirect["new_path"]
                    )

            if settings.APPEND_SLASH and not request.path.endswith("/"):
                # Try appending a trailing slash.
                path_len = len(request.path)
                slashed_full_path = full_path[:path_len] + "/" + full_path[path_len:]

                if redirect["old_path"] == slashed_full_path:
                    self.increment_redirect(redirect["id"])
                    if redirect["new_path"].startswith("http"):
                        return http.HttpResponsePermanentRedirect(redirect["new_path"])
                    else:
                        return http.HttpResponsePermanentRedirect(
                            http_host + redirect["new_path"]
                        )

        reg_redirects = cache.get(DJANGO_REGEX_REDIRECTS_CACHE_REGEX_KEY)
        if reg_redirects is None:
            reg_redirects = list(
                Redirect.objects.filter(regular_expression=True)
                .order_by("fallback_redirect")
                .values()
            )
            cache.set(
                DJANGO_REGEX_REDIRECTS_CACHE_REGEX_KEY,
                reg_redirects,
                DJANGO_REGEX_REDIRECTS_CACHE_TIMEOUT,
            )

        for redirect in reg_redirects:
            try:
                old_path = re.compile(redirect["old_path"], re.IGNORECASE)
            except re.error:
                # old_path does not compile into regex, ignore it and move on to the next one
                continue

            if re.match(redirect["old_path"], full_path):
                self.increment_redirect(redirect["id"])
                # Convert $1 into \1 (otherwise users would have to enter \1 via the admin
                # which would have to be escaped)
                new_path = redirect["new_path"].replace("$", "\\")
                replaced_path = re.sub(old_path, new_path, full_path)
                if redirect["new_path"].startswith("http"):
                    return http.HttpResponsePermanentRedirect(replaced_path)
                else:
                    return http.HttpResponsePermanentRedirect(http_host + replaced_path)

        # No redirect was found. Return the response.
        return response
