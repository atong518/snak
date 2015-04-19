# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0017_auto_20150419_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='started_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 19, 19, 20, 37, 941464), null=True, verbose_name=b'started at', blank=True),
            preserve_default=True,
        ),
    ]
