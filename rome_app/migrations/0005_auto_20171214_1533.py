# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-14 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rome_app', '0004_auto_20171207_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biography',
            name='alternate_names',
            field=models.CharField(blank=True, help_text='Optional: enter alternate names separated by a semi-colon', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='biography',
            name='birth_date',
            field=models.CharField(blank=True, help_text='Optional: enter birth date as yyyy-mm-dd (for sorting and filtering)', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='biography',
            name='death_date',
            field=models.CharField(blank=True, help_text='Optional: enter death date as yyyy-mm-dd', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='biography',
            name='external_id',
            field=models.CharField(blank=True, help_text='Optional: enter Ulan id in the form of a URL; if there is no Ulan id, enter LCCN in the form of a URL', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='biography',
            name='name',
            field=models.CharField(help_text='Enter name as it appears in the book metadata', max_length=254),
        ),
        migrations.AlterField(
            model_name='biography',
            name='roles',
            field=models.CharField(blank=True, help_text='Optional: enter roles, separated by a semi-colon', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='biography',
            name='trp_id',
            field=models.CharField(blank=True, help_text='Optional: This value will be auto-generated by the server if the field is left blank or non-unique value is entered', max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='essay',
            name='people',
            field=models.ManyToManyField(blank=True, help_text='List of people associated with this essay.', to='rome_app.Biography'),
        ),
        migrations.AlterField(
            model_name='essay',
            name='pids',
            field=models.CharField(blank=True, help_text='Comma-separated list of pids for books or prints associated with this essay.', max_length=254, null=True),
        ),
    ]
