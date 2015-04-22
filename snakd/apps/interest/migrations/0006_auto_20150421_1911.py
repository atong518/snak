# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0005_interest_gender'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='interest',
            options={'ordering': ['name']},
        ),
    ]
