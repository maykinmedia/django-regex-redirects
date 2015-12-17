# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('old_path', models.CharField(help_text="This should be an absolute path, excluding the domain name. Example: '/events/search/'.", unique=True, max_length=200, verbose_name='redirect from', db_index=True)),
                ('new_path', models.CharField(help_text="This can be either an absolute path (as above) or a full URL starting with 'http://'.", max_length=200, verbose_name='redirect to', blank=True)),
                ('regular_expression', models.BooleanField(default=False, help_text='If checked, the redirect-from and redirect-to fields will also be processed using regular expressions when matching incoming requests.<br>Example: <strong>/projects/.* -> /#!/projects</strong> will redirect everyone visiting a page starting with /projects/<br>Example: <strong>/projects/(.*) -> /#!/projects/$1</strong> will turn /projects/myproject into /#!/projects/myproject<br><br>Invalid regular expressions will be ignored.', verbose_name='Match using regular expressions')),
                ('fallback_redirect', models.BooleanField(default=False, help_text="This redirect is only matched after all other redirects have failed to match.<br>This allows us to define a general 'catch-all' that is only used as a fallback after more specific redirects have been attempted.", verbose_name='Fallback redirect')),
                ('nr_times_visited', models.IntegerField(default=0, help_text='Is incremented each time a visitor hits this redirect')),
            ],
            options={
                'ordering': ('fallback_redirect', 'regular_expression', 'old_path'),
                'verbose_name': 'redirect',
                'verbose_name_plural': 'redirects',
            },
        ),
    ]
