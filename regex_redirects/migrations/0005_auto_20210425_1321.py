# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regex_redirects', '0004_auto_20170512_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redirect',
            name='old_path',
            field=models.CharField(db_index=True, help_text="This should be an absolute path, excluding the domain name. Example: '/events/search/'.", max_length=512, verbose_name='redirect from'),
        ),
    ]
