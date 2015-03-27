# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import snakd.apps.interest.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Test', max_length=50)),
                ('tooltip', models.CharField(max_length=50, null=True)),
                ('weight', models.IntegerField(default=0)),
                ('hidden', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(related_name='children', to='interest.Interest', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InterestMatrix',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('matrix', snakd.apps.interest.models.SerializedDataField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
