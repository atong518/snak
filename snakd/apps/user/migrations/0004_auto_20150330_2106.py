# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20150330_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegeuser',
            name='next_match',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 30, 21, 6, 36, 473722)),
            preserve_default=True,
        ),
    ]
