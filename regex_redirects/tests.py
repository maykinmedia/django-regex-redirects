from __future__ import unicode_literals

from unittest.case import skipUnless

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import six
from django.core.cache import cache

from .models import Redirect
from .middleware import DJANGO_REGEX_REDIRECTS_CACHE_KEY, DJANGO_REGEX_REDIRECTS_CACHE_REGEX_KEY


class RegexRedirectTests(TestCase):

    def setUp(self):
        cache.delete(DJANGO_REGEX_REDIRECTS_CACHE_KEY)
        cache.delete(DJANGO_REGEX_REDIRECTS_CACHE_REGEX_KEY)

    def test_model(self):
        r1 = Redirect.objects.create(
            old_path='/initial', new_path='/new_target')
        self.assertEqual(six.text_type(r1), "/initial ---> /new_target")

    def test_redirect(self):
        Redirect.objects.create(
            old_path='/initial', new_path='/new_target')
        response = self.client.get('/initial')
        self.assertRedirects(response,
            '/new_target', status_code=301, target_status_code=404)

    @override_settings(APPEND_SLASH=True)
    def test_redirect_with_append_slash(self):
        Redirect.objects.create(
            old_path='/initial/', new_path='/new_target/')
        response = self.client.get('/initial')
        self.assertRedirects(response,
            '/new_target/', status_code=301, target_status_code=404)

    @override_settings(APPEND_SLASH=True)
    def test_redirect_with_append_slash_and_query_string(self):
        Redirect.objects.create(
            old_path='/initial/?foo', new_path='/new_target/')
        response = self.client.get('/initial?foo')
        self.assertRedirects(response,
            '/new_target/', status_code=301, target_status_code=404)

    def test_regular_expression(self):
        Redirect.objects.create(
            old_path='/news/index/(\d+)/(.*)/',
            new_path='/my/news/$2/',
            regular_expression=True)
        response = self.client.get('/news/index/12345/foobar/')
        self.assertRedirects(response,
                             '/my/news/foobar/',
                             status_code=301, target_status_code=404)
        redirect = Redirect.objects.get(regular_expression=True)

    def test_fallback_redirects(self):
        """
        Ensure redirects with fallback_redirect set are the last evaluated
        """
        Redirect.objects.create(
            old_path='/project/foo',
            new_path='/my/project/foo')

        Redirect.objects.create(
            old_path='/project/foo/(.*)',
            new_path='/my/project/foo/$1',
            regular_expression=True)

        Redirect.objects.create(
            old_path='/project/(.*)',
            new_path='/projects',
            regular_expression=True,
            fallback_redirect=True)

        Redirect.objects.create(
            old_path='/project/bar/(.*)',
            new_path='/my/project/bar/$1',
            regular_expression=True)

        Redirect.objects.create(
            old_path='/project/bar',
            new_path='/my/project/bar')

        Redirect.objects.create(
            old_path='/second_project/.*',
            new_path='http://example.com/my/second_project/bar/',
            regular_expression=True)
        
        Redirect.objects.create(
            old_path='/third_project/(.*)',
            new_path='http://example.com/my/third_project/bar/$1',
            regular_expression=True)

        response = self.client.get('/project/foo')
        self.assertRedirects(response,
                             '/my/project/foo',
                             status_code=301, target_status_code=404)

        response = self.client.get('/project/bar')
        self.assertRedirects(response,
                             '/my/project/bar',
                             status_code=301, target_status_code=404)

        response = self.client.get('/project/bar/details')
        self.assertRedirects(response,
                             '/my/project/bar/details',
                             status_code=301, target_status_code=404)

        response = self.client.get('/project/foobar')
        self.assertRedirects(response,
                             '/projects',
                             status_code=301, target_status_code=404)

        response = self.client.get('/project/foo/details')
        self.assertRedirects(response,
                             '/my/project/foo/details',
                             status_code=301, target_status_code=404)

        response = self.client.get('/second_project/details')
        self.assertRedirects(response,
                             'http://example.com/my/second_project/bar/',
                             status_code=301, target_status_code=404)

        response = self.client.get('/third_project/details')
        self.assertRedirects(response,
                             'http://example.com/my/third_project/bar/details',
                             status_code=301, target_status_code=404)
