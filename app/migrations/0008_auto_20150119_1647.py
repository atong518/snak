# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_genericuser_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericuser',
            name='is_active',
            field=models.NullBooleanField(default=False),
            preserve_default=True,
        ),
    ]
