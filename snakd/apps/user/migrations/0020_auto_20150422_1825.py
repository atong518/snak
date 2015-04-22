# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_auto_20150421_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegeuser',
            name='next_match',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 22, 18, 25, 16, 402366)),
            preserve_default=True,
        ),
    ]
