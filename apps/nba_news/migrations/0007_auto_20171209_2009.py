# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-09 20:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nba_news', '0006_auto_20171209_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
