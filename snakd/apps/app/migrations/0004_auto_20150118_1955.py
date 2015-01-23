# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_genericuser_activation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericuser',
            name='activation_code',
            field=models.CharField(max_length=250),
            preserve_default=True,
        ),
    ]
