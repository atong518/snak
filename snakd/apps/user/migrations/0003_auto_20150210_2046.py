# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0003_interest_hidden'),
        ('user', '0002_collegeuser_max_match_frequency'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericuser',
            name='interests',
            field=models.ManyToManyField(to='interest.Interest', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='collegeuser',
            name='max_match_frequency',
            field=models.IntegerField(max_length=200),
            preserve_default=True,
        ),
    ]
