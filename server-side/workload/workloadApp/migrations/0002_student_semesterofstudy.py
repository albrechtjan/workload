# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workloadApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='semesterOfStudy',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
