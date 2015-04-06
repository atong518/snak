# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20150406_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericuser',
            name='contact_comments',
            field=models.CharField(max_length=1000, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='collegeuser',
            name='next_match',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 6, 19, 25, 4, 587282)),
            preserve_default=True,
        ),
    ]
