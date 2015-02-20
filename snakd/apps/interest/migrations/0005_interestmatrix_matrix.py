# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import snakd.apps.interest.models


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0004_interestmatrix'),
    ]

    operations = [
        migrations.AddField(
            model_name='interestmatrix',
            name='matrix',
            field=snakd.apps.interest.models.SerializedDataField(null=True),
            preserve_default=True,
        ),
    ]
