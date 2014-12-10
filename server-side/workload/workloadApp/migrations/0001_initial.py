# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('semester', models.CharField(max_length=9)),
                ('name', models.CharField(max_length=200)),
                ('startDay', models.DateField()),
                ('endDay', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lectures', models.ManyToManyField(to='workloadApp.Lecture', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkingHoursEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hoursInLecture', models.FloatField(default=0)),
                ('hoursForHomework', models.FloatField(default=0)),
                ('hoursStudying', models.FloatField(default=0)),
                ('week', models.DateField()),
                ('lecture', models.ForeignKey(to='workloadApp.Lecture')),
                ('student', models.ForeignKey(to='workloadApp.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
