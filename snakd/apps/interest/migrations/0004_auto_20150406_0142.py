# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0003_auto_20150330_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='weight',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
