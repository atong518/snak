# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0006_auto_20150421_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='interest',
            name='freq',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
