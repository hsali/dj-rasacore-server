# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 06:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rasacore', '0013_auto_20171116_0609'),
    ]

    operations = [
        migrations.AddField(
            model_name='intentusersaysentities',
            name='synonyms',
            field=models.CharField(blank=True, help_text='Add multiple value synonyms separated by commas', max_length=400, null=True),
        ),
    ]
