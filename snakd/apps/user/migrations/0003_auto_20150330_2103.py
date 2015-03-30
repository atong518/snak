# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20150330_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegeuser',
            name='next_match',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 30, 21, 3, 21, 3571)),
            preserve_default=True,
        ),
    ]
