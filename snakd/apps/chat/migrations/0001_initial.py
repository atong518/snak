# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('sent_at', models.DateTimeField(default=datetime.datetime(2015, 3, 30, 20, 50, 39, 195284), null=True, verbose_name=b'sent at', blank=True)),
                ('sender', models.ForeignKey(related_name='sent_messages', verbose_name=b'Sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-sent_at'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(default=b'', max_length=200, blank=True)),
                ('started_at', models.DateTimeField(default=datetime.datetime(2015, 3, 30, 20, 50, 39, 194102), null=True, verbose_name=b'started at', blank=True)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(to='chat.Thread'),
            preserve_default=True,
        ),
    ]
