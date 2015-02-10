# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20150210_2103'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thread',
            old_name='member',
            new_name='members',
        ),
        migrations.AddField(
            model_name='thread',
            name='subject',
            field=models.CharField(default='test', max_length=200),
            preserve_default=False,
        ),
    ]
