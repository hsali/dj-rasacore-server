# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 06:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rasacore', '0012_auto_20171116_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='intentusersaysentities',
            name='end',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='intentusersaysentities',
            name='start',
            field=models.IntegerField(default=0),
        ),
    ]
