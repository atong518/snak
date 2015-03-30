# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20150313_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sent_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 30, 19, 21, 14, 149290), null=True, verbose_name=b'sent at', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thread',
            name='started_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 30, 19, 21, 14, 147870), null=True, verbose_name=b'started at', blank=True),
            preserve_default=True,
        ),
    ]
