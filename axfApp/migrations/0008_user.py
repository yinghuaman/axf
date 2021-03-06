# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-02-21 04:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('axfApp', '0007_goods'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userAccount', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('userPhone', models.CharField(max_length=15)),
                ('userRank', models.IntegerField()),
                ('email', models.CharField(max_length=64, unique=True)),
                ('userToken', models.CharField(max_length=50)),
                ('icon', models.CharField(max_length=150)),
                ('is_delete', models.BooleanField(default=False)),
            ],
        ),
    ]
