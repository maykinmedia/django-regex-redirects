# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regex_redirects', '0002_auto_20151217_1938'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='redirect',
            unique_together=set([]),
        ),
    ]
