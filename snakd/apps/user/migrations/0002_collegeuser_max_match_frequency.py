# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='collegeuser',
            name='max_match_frequency',
            field=models.IntegerField(default=2592000, max_length=200, choices=[(0, b'Unlimited'), (864000, b'1 per day'), (2592000, b'1 every 3 days'), (6048000, b'1 per week'), (12096000, b'1 every 2 weeks')]),
            preserve_default=True,
        ),
    ]
