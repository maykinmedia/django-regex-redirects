# -*- coding: utf-8 -*-
from distutils.core import setup

from setuptools import find_packages

setup(
    name='django-regex-redirects',
    version='0.0.9',
    author=u'Alex de Landgraaf',
    author_email='alex@maykinmedia.nl',
    packages=find_packages(),
    url='https://github.com/maykinmedia/django-regex-redirects',
    license='BSD licence, see LICENCE.txt',
    description='Django redirects, with regular expressions',
    include_package_data=True,
)
