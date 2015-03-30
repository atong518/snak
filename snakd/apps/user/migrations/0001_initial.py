# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('email', models.EmailField(unique=True, max_length=222)),
                ('firstname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=200)),
                ('homecountry', models.CharField(max_length=200)),
                ('homestate', models.CharField(max_length=200, null=True, blank=True)),
                ('activation_code', models.CharField(max_length=250)),
                ('is_active', models.NullBooleanField(default=False)),
                ('gender', models.CharField(default=b'gender is a construct', max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CollegeUser',
            fields=[
                ('genericuser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bio', models.CharField(max_length=500)),
                ('max_match_frequency', models.IntegerField(default=0)),
                ('next_match', models.DateTimeField(default=datetime.datetime(2015, 3, 30, 20, 50, 39, 191857))),
            ],
            options={
                'abstract': False,
            },
            bases=('user.genericuser',),
        ),
        migrations.CreateModel(
            name='ProspieUser',
            fields=[
                ('genericuser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('user.genericuser',),
        ),
        migrations.AddField(
            model_name='collegeuser',
            name='matches',
            field=models.ManyToManyField(related_name='matches', null=True, to='user.ProspieUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericuser',
            name='interests',
            field=models.ManyToManyField(related_name='user_set', null=True, to='interest.Interest'),
            preserve_default=True,
        ),
    ]
