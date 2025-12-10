django-regex-redirects
======================
:Version: 0.7.1
:Source: https://github.com/maykinmedia/django-regex-redirects
:Keywords: Django, regex
:PythonVersion: 3.8

|build-status| |code-quality| |black| |coverage|

|python-versions| |django-versions| |pypi-version|


Django redirects, with regular expressions. It is a modified version of
django.contrib.redirects.

Features
========

-  Redirect your visitors using regular expressions
-  Configurable via the admin
-  Redirects are exportable as .csv

https://pypi.org/pypi/django-regex-redirects

Install
=======

``pip install django-regex-redirects``

Add ``regex_redirects`` to your ``INSTALLED_APPS``:

.. code:: python

   INSTALLED_APPS = (
     ...
     "regex_redirects",
     ...
   )

Add the middleware to your ``MIDDLEWARE``:

.. code:: python

   MIDDLEWARE = [
     "regex_redirects.middleware.RedirectFallbackMiddleware"
     ...
   ]

Run ``manage.py migrate`` and you’re good to go!

.. |build-status| image:: https://github.com/maykinmedia/django-regex-redirects/actions/workflows/ci.yml/badge.svg
    :alt: Build status
    :target: https://github.com/maykinmedia/django-regex-redirects/actions/workflows/ci.yml

.. |code-quality| image:: https://github.com/maykinmedia/django-regex-redirects/actions/workflows/code-quality.yml/badge.svg
     :alt: Code quality checks
     :target: https://github.com/maykinmedia/django-regex-redirects/actions/workflows/code-quality.yml

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |coverage| image:: https://codecov.io/gh/maykinmedia/django-regex-redirects/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/django-regex-redirects
    :alt: Coverage status


.. |python-versions| image:: https://img.shields.io/pypi/pyversions/django-regex-redirects.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/django-regex-redirects.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/django-regex-redirects.svg
    :target: https://pypi.org/project/django-regex-redirects/
