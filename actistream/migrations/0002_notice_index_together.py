# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 15:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('actistream', '0001_initial'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='notice',
            index_together=set([('user', 'read_at')]),
        ),
    ]