# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-08 15:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0012_auto_20160407_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='minutes',
            name='approved_by',
        ),
    ]
