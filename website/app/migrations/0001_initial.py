# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-28 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('user_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=1500)),
                ('secret', models.CharField(max_length=1500)),
                ('otp_salt', models.CharField(max_length=16)),
                ('passwd_salt', models.CharField(max_length=50)),
                ('f_name', models.CharField(max_length=20)),
                ('l_name', models.CharField(max_length=20)),
                ('email_address', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='RequestQR',
            fields=[
                ('request_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('email_address', models.EmailField(max_length=254)),
                ('expiry_time', models.CharField(max_length=20)),
                ('reset', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SessionData',
            fields=[
                ('user_id', models.CharField(max_length=50)),
                ('random_nonce', models.CharField(max_length=20)),
                ('expiry_time', models.CharField(max_length=20)),
                ('other_data', models.TextField(null=True)),
                ('session_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
    ]
