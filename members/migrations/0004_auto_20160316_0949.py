# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-16 09:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_auto_20160310_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overview', models.BooleanField(default=False)),
                ('reminder', models.BooleanField(default=False)),
                ('organizations', models.ManyToManyField(to='members.Organization')),
            ],
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'permissions': [('change_groups', 'Can change user groups'), ('list_persons', 'Can view persons')], 'verbose_name': 'person'},
        ),
        migrations.AddField(
            model_name='preferences',
            name='person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
