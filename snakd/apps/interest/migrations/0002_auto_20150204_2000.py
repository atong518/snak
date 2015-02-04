# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interest',
            name='name',
            field=models.CharField(default=b'Test', max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='interest',
            name='tooltip',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='interest',
            name='weight',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
