# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_auto_20150422_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegeuser',
            name='next_match',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 22, 19, 53, 7, 474689)),
            preserve_default=True,
        ),
    ]
