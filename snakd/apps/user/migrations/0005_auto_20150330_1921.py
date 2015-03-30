# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20150313_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericuser',
            name='gender',
            field=models.CharField(default=b'gender is a construct', max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='collegeuser',
            name='next_match',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 30, 19, 21, 14, 145620)),
            preserve_default=True,
        ),
    ]
