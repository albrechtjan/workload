# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workloadApp', '0004_workinghoursentry_semesterofstudy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workinghoursentry',
            name='semesterOfStudy',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
