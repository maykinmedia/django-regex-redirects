django-regex-redirects [![Build Status](https://travis-ci.org/maykinmedia/django-regex-redirects.svg?branch=master)](https://travis-ci.org/maykinmedia/django-regex-redirects)
======================

Django redirects, with regular expressions. It is a modified version of django.contrib.redirects.

Features
========

 * Redirect your visitors using regular expressions
 * Configurable via the admin
 * Counts the number of visitors
 * Redirects are exportable as .csv
 
https://pypi.python.org/pypi/django-regex-redirects

Install
=======

```pip install django-regex-redirects``` or ```python setup.py install```

Add regex_redirects to your INSTALLED_APPS:

```
INSTALLED_APPS = (
  ...
  'regex_redirects',
  ...
)
```

Add the middleware to your MIDDLEWARE_CLASSES:

```
MIDDLEWARE_CLASSES = [
  'regex_redirects.middleware.RedirectFallbackMiddleware'
  ...
]
```

Run manage.py migrate and you're good to go!




