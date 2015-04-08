# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0004_auto_20150406_0142'),
    ]

    operations = [
        migrations.AddField(
            model_name='interest',
            name='gender',
            field=models.CharField(default=b'gender is a construct', max_length=50),
            preserve_default=True,
        ),
    ]
