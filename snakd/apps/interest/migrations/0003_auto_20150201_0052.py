# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0002_interest_interest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interest',
            name='interest',
        ),
        migrations.AddField(
            model_name='interest',
            name='parent',
            field=models.ForeignKey(related_name='children', to='interest.Interest', null=True),
            preserve_default=True,
        ),
    ]
