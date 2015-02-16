# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='started_at',
            field=models.DateTimeField(null=True, verbose_name=b'started at', blank=True),
            preserve_default=True,
        ),
    ]
