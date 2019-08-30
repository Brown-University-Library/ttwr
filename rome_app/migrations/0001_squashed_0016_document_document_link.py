# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-08-30 09:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('rome_app', '0001_initial'), ('rome_app', '0002_auto_20170829_1009'), ('rome_app', '0003_auto_20171206_0827'), ('rome_app', '0004_auto_20171207_1100'), ('rome_app', '0005_auto_20171214_1533'), ('rome_app', '0006_shop'), ('rome_app', '0007_shop_slug'), ('rome_app', '0008_auto_20190710_1051'), ('rome_app', '0009_auto_20190710_1053'), ('rome_app', '0010_auto_20190807_1026'), ('rome_app', '0011_auto_20190811_2107'), ('rome_app', '0012_document_slug'), ('rome_app', '0013_auto_20190812_1200'), ('rome_app', '0014_document_summary'), ('rome_app', '0015_document_consagra'), ('rome_app', '0016_document_document_link')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Biography',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text=b'Enter name as it appears in the book metadata', max_length=254)),
                ('trp_id', models.CharField(blank=True, help_text=b'Optional: This value will be auto-generated by the server if the field is left blank or non-unique value is entered', max_length=15, unique=True)),
                ('alternate_names', models.CharField(blank=True, help_text=b'Optional: enter alternate names separated by a semi-colon', max_length=254, null=True)),
                ('external_id', models.CharField(blank=True, help_text=b'Optional: enter Ulan id in the form of a URL; if there is no Ulan id, enter LCCN in the form of a URL', max_length=254, null=True)),
                ('birth_date', models.CharField(blank=True, help_text=b'Optional: enter birth date as yyyy-mm-dd (for sorting and filtering)', max_length=25, null=True)),
                ('death_date', models.CharField(blank=True, help_text=b'Optional: enter death date as yyyy-mm-dd', max_length=25, null=True)),
                ('roles', models.CharField(blank=True, help_text=b'Optional: enter roles, separated by a semi-colon', max_length=254, null=True)),
                ('bio', models.TextField()),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'biographies',
            },
        ),
        migrations.CreateModel(
            name='Essay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=191)),
                ('author', models.CharField(max_length=254)),
                ('title', models.CharField(max_length=254)),
                ('text', models.TextField()),
                ('pids', models.CharField(blank=True, help_text='Comma-separated list of pids for books or prints associated with this essay.', max_length=254, null=True)),
                ('people', models.ManyToManyField(blank=True, help_text='List of people associated with this essay.', to='rome_app.Biography')),
                ('is_note', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50, unique=True)),
                ('external_id', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50, unique=True)),
                ('external_id', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Static',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=254)),
                ('text', models.TextField()),
            ],
        ),
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
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=254)),
                ('text', models.TextField()),
                ('pids', models.CharField(blank=True, help_text='Comma-separated list of pids for books or prints associated with this shop.', max_length=254, null=True)),
                ('people', models.ManyToManyField(blank=True, help_text='List of people associated with this Shop.', to='rome_app.Biography')),
                ('slug', models.SlugField(default='', max_length=191)),
                ('family', models.CharField(blank=True, help_text='Enter Family associated with shop', max_length=254, null=True)),
                ('end_date', models.CharField(blank=True, help_text='Optional: enter death date as yyyy-mm-dd', max_length=25, null=True)),
                ('start_date', models.CharField(blank=True, help_text='Optional: enter birth date as yyyy-mm-dd (for sorting and filtering)', max_length=25, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='essay',
            name='shops',
            field=models.ManyToManyField(blank=True, help_text='List of shops associated with this essay.', to='rome_app.Shop'),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=254)),
                ('text', models.TextField()),
                ('document_file', models.FileField(blank=True, upload_to='')),
                ('people', models.ManyToManyField(blank=True, help_text='List of people associated with this essay.', to='rome_app.Biography')),
                ('slug', models.SlugField(default='doc', max_length=191)),
                ('summary', models.TextField(default='')),
                ('consagra', models.BooleanField(default=0)),
                ('document_link', models.URLField(default='')),
            ],
        ),
        migrations.AddField(
            model_name='shop',
            name='documents',
            field=models.ManyToManyField(blank=True, help_text='List of documents associated with this shop.', to='rome_app.Document'),
        ),
    ]
