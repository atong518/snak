# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0024_auto_20150422_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='started_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 22, 20, 42, 25, 585294), null=True, verbose_name=b'started at', blank=True),
            preserve_default=True,
        ),
    ]
