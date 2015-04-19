# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0016_auto_20150419_1914'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={},
        ),
        migrations.RemoveField(
            model_name='message',
            name='sent_at',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='started_at',
        ),
        migrations.AddField(
            model_name='message',
            name='timestamp',
            field=models.BigIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thread',
            name='timestamp',
            field=models.BigIntegerField(null=True),
            preserve_default=True,
        ),
    ]
