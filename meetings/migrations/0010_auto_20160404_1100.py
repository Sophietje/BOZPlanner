# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-04 11:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0009_auto_20160323_1107'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meeting',
            options={'permissions': [('list_meetings', 'Can list meetings'), ('list_meetings_organization', 'Can list meetings of her organization'), ('list_meetings_all', 'Can list all meetings'), ('view_organization', 'Can view meetings from own organization'), ('view_all', 'Can view all meetings')], 'verbose_name': 'Meeting'},
        ),
    ]
