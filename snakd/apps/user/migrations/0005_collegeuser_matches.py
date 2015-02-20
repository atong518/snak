# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20150220_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='collegeuser',
            name='matches',
            field=models.ManyToManyField(related_name='matches', null=True, to='user.ProspieUser'),
            preserve_default=True,
        ),
    ]
