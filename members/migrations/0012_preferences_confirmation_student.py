# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-28 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_auto_20160328_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='preferences',
            name='confirmation_student',
            field=models.BooleanField(default=True, verbose_name='Receive confirmation mail when adding yourself to a meeting'),
        ),
    ]
