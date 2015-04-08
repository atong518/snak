# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20150408_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegeuser',
            name='next_match',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 8, 20, 59, 58, 268089)),
            preserve_default=True,
        ),
    ]
