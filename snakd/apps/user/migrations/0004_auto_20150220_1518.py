# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20150210_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericuser',
            name='interests',
            field=models.ManyToManyField(related_name='user_set', null=True, to='interest.Interest'),
            preserve_default=True,
        ),
    ]
