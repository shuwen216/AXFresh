# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-10-07 22:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0009_auto_20201006_0435'),
    ]

    operations = [
        migrations.CreateModel(
            name='AXFUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_username', models.CharField(max_length=64, unique=True)),
                ('u_password', models.CharField(max_length=255)),
                ('u_email', models.CharField(max_length=64, unique=True)),
                ('u_icon', models.ImageField(upload_to='icons/%Y/%m/%d/')),
                ('is_active', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'axf_user',
            },
        ),
    ]
