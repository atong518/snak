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
            name='interest',
            field=models.ForeignKey(to='interest.Fake', null=True),
            preserve_default=True,
        ),
    ]
