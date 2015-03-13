# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='subject',
            field=models.CharField(default=b'', max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
