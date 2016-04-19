# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regex_redirects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redirect',
            name='new_path',
            field=models.CharField(help_text="This can be either an absolute path (as above) or a full URL starting with 'http://'.", max_length=2000, verbose_name='redirect to', blank=True),
        ),
        migrations.AlterField(
            model_name='redirect',
            name='old_path',
            field=models.CharField(help_text="This should be an absolute path, excluding the domain name. Example: '/events/search/'.", max_length=2000, verbose_name='redirect from', db_index=True),
        ),
    ]
