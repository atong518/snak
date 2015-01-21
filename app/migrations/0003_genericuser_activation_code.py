# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150116_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericuser',
            name='activation_code',
            field=models.CharField(max_length=250, blank=True),
            preserve_default=True,
        ),
    ]
