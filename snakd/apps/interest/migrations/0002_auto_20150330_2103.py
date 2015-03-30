# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='tooltip',
            field=models.CharField(max_length=500, null=True),
            preserve_default=True,
        ),
    ]
