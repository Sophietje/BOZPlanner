# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-18 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20160316_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preferences',
            name='organizations',
            field=models.ManyToManyField(blank=True, to='members.Organization'),
        ),
    ]
