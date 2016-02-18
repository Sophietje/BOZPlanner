# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-17 21:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0003_auto_20160217_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='planner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='planner', to='members.Person'),
        ),
    ]
