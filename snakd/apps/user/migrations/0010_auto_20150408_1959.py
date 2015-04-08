# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20150408_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericuser',
            name='user_email',
            field=models.CharField(max_length=222, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='collegeuser',
            name='next_match',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 8, 19, 59, 37, 886780)),
            preserve_default=True,
        ),
    ]
