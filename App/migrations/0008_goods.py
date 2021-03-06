# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-10-06 04:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_foodtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productid', models.IntegerField(default=1)),
                ('productimg', models.CharField(max_length=255)),
                ('productname', models.CharField(max_length=128)),
                ('productlongname', models.CharField(max_length=255)),
                ('isxf', models.BooleanField(default=False)),
                ('pmdesc', models.BooleanField(default=False)),
                ('specifies', models.CharField(max_length=64)),
                ('spice', models.FloatField(default=0)),
                ('marketprice', models.FloatField(default=1)),
                ('categoryid', models.IntegerField(default=1)),
                ('childcid', models.IntegerField(default=1)),
                ('childcidname', models.CharField(max_length=128)),
                ('dealerid', models.IntegerField(default=1)),
                ('storenums', models.IntegerField(default=1)),
                ('productnum', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'axf_goods',
            },
        ),
    ]
