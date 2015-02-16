# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20150210_2101'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='conversation',
            new_name='thread',
        ),
    ]
