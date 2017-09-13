# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-13 07:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fias', '0016_addrobjindex_search_vector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addrobjindex',
            name='aolevel',
            field=models.PositiveSmallIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='addrobjindex',
            name='item_weight',
            field=models.PositiveSmallIntegerField(db_index=True, default=64),
        ),
    ]