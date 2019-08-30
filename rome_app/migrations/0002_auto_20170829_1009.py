# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rome_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Static',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=254)),
                ('text', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='essay',
            name='is_note',
            field=models.BooleanField(default=False),
        ),
    ]
