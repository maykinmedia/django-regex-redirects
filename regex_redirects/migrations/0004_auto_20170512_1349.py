# -*- coding: utf-8 -*-
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("regex_redirects", "0002_auto_20151217_1938"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="redirect",
            unique_together=set([]),
        ),
    ]
