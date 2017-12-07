# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 03:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('nba_news', '0004_auto_20171206_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='published_on',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]