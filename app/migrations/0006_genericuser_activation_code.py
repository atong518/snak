# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_genericuser_activation_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericuser',
            name='activation_code',
            field=models.CharField(default='blank', max_length=250),
            preserve_default=False,
        ),
    ]
