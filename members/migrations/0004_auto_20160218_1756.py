# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-18 16:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_auto_20160218_1727'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'permissions': [('groups', 'Can change user groups')], 'verbose_name': 'person'},
        ),
    ]
