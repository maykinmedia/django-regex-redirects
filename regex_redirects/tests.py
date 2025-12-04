from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from .middleware import (
    DJANGO_REGEX_REDIRECTS_CACHE_KEY,
    DJANGO_REGEX_REDIRECTS_CACHE_REGEX_KEY,
)
from .models import Redirect


class RegexRedirectTests(TestCase):

    def setUp(self):
        cache.delete(DJANGO_REGEX_REDIRECTS_CACHE_KEY)
        cache.delete(DJANGO_REGEX_REDIRECTS_CACHE_REGEX_KEY)

    def test_model(self):
        r1 = Redirect.objects.create(old_path="/initial", new_path="/new_target")
        self.assertEqual(str(r1), "/initial ---> /new_target")

    def test_redirect(self):
        redirect = Redirect.objects.create(old_path="/initial", new_path="/new_target")
        self.assertEqual(redirect.nr_times_visited, 0)
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            response = self.client.get("/initial")
        self.assertEqual(len(callbacks), 1)
        self.assertRedirects(
            response, "/new_target", status_code=301, target_status_code=404
        )
        redirect.refresh_from_db()
        self.assertEqual(redirect.nr_times_visited, 1)

    @override_settings(APPEND_SLASH=True)
    def test_redirect_with_append_slash(self):
        redirect = Redirect.objects.create(
            old_path="/initial/", new_path="/new_target/"
        )
        self.assertEqual(redirect.nr_times_visited, 0)
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            response = self.client.get("/initial")
        self.assertEqual(len(callbacks), 1)
        self.assertRedirects(
            response, "/new_target/", status_code=301, target_status_code=404
        )
        redirect.refresh_from_db()
        self.assertEqual(redirect.nr_times_visited, 1)

    @override_settings(APPEND_SLASH=True)
    def test_redirect_with_append_slash_and_query_string(self):
        Redirect.objects.create(old_path="/initial/?foo", new_path="/new_target/")
        response = self.client.get("/initial?foo")
        self.assertRedirects(
            response, "/new_target/", status_code=301, target_status_code=404
        )

    def test_regular_expression(self):
        Redirect.objects.create(
            old_path=r"/news/index/(\d+)/(.*)/",
            new_path="/my/news/$2/",
            regular_expression=True,
        )
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            response = self.client.get("/news/index/12345/foobar/")
        self.assertEqual(len(callbacks), 1)
        self.assertRedirects(
            response, "/my/news/foobar/", status_code=301, target_status_code=404
        )
        redirect = Redirect.objects.get(regular_expression=True)
        redirect.refresh_from_db()
        self.assertEqual(redirect.nr_times_visited, 1)

    def test_fallback_redirects(self):
        """
        Ensure redirects with fallback_redirect set are the last evaluated
        """
        Redirect.objects.create(old_path="/project/foo", new_path="/my/project/foo")

        Redirect.objects.create(
            old_path="/project/foo/(.*)",
            new_path="/my/project/foo/$1",
            regular_expression=True,
        )

        Redirect.objects.create(
            old_path="/project/(.*)",
            new_path="/projects",
            regular_expression=True,
            fallback_redirect=True,
        )

        Redirect.objects.create(
            old_path="/project/bar/(.*)",
            new_path="/my/project/bar/$1",
            regular_expression=True,
        )

        Redirect.objects.create(old_path="/project/bar", new_path="/my/project/bar")

        Redirect.objects.create(
            old_path="/second_project/.*",
            new_path="http://example.com/my/second_project/bar/",
            regular_expression=True,
        )

        Redirect.objects.create(
            old_path="/third_project/(.*)",
            new_path="http://example.com/my/third_project/bar/$1",
            regular_expression=True,
        )

        response = self.client.get("/project/foo")
        self.assertRedirects(
            response, "/my/project/foo", status_code=301, target_status_code=404
        )

        response = self.client.get("/project/bar")
        self.assertRedirects(
            response, "/my/project/bar", status_code=301, target_status_code=404
        )

        response = self.client.get("/project/bar/details")
        self.assertRedirects(
            response, "/my/project/bar/details", status_code=301, target_status_code=404
        )

        response = self.client.get("/project/foobar")
        self.assertRedirects(
            response, "/projects", status_code=301, target_status_code=404
        )

        response = self.client.get("/project/foo/details")
        self.assertRedirects(
            response, "/my/project/foo/details", status_code=301, target_status_code=404
        )

        response = self.client.get("/second_project/details")
        self.assertRedirects(
            response,
            "http://example.com/my/second_project/bar/",
            status_code=301,
            target_status_code=404,
        )

        response = self.client.get("/third_project/details")
        self.assertRedirects(
            response,
            "http://example.com/my/third_project/bar/details",
            status_code=301,
            target_status_code=404,
        )


class RedirectExportAdminActionTest(TestCase):

    def setUp(self):

        self.superuser = User.objects.create_superuser("exporter_man")
        self.client.force_login(self.superuser)

        self.redirect_1 = Redirect.objects.create(
            old_path="/initial", new_path="/new_target"
        )
        self.redirect_2 = Redirect.objects.create(
            old_path=r"/news/index/(\d+)/(.*)/",
            new_path="/my/news/$2/",
            regular_expression=True,
        )

        self.url = reverse("admin:regex_redirects_redirect_changelist")

    def test_simple(self):
        data = {
            "action": "export_as_csv",
            "_selected_action": [self.redirect_1.pk, self.redirect_2.pk],
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"), "attachment; filename=redirect.csv"
        )
