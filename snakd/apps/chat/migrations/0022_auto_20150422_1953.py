# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0021_auto_20150422_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='started_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 22, 19, 53, 7, 490477), null=True, verbose_name=b'started at', blank=True),
            preserve_default=True,
        ),
    ]
