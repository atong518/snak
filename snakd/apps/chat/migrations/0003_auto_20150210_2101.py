# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_thread_started_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='thread',
            new_name='conversation',
        ),
    ]
