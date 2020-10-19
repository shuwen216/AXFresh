# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-10-12 07:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0010_axfuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_goods_num', models.IntegerField(default=1)),
                ('c_is_selected', models.BooleanField(default=True)),
                ('c_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.Goods')),
                ('c_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.AXFUser')),
            ],
            options={
                'db_table': 'axf_cart',
            },
        ),
    ]