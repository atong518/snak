# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sent_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 30, 21, 1, 41, 926315), null=True, verbose_name=b'sent at', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thread',
            name='started_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 30, 21, 1, 41, 925118), null=True, verbose_name=b'started at', blank=True),
            preserve_default=True,
        ),
    ]
