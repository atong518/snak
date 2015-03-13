# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20150313_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='collegeuser',
            name='max_match_frequency',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='collegeuser',
            name='next_match',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 13, 12, 32, 55, 250856)),
            preserve_default=True,
        ),
    ]
