# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0002_auto_20150204_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='interest',
            name='hidden',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
