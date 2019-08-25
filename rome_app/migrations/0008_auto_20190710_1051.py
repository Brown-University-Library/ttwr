# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-07-10 10:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rome_app', '0007_shop_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='essay',
            name='shops',
            field=models.ManyToManyField(blank=True, help_text='List of shops associated with this essay.', to='rome_app.Shop'),
        ),
        migrations.AddField(
            model_name='shop',
            name='roles',
            field=models.CharField(blank=True, help_text='Enter Family associated with shop', max_length=254, null=True),
        ),
    ]
