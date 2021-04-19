# Generated by Django 3.2 on 2021-04-15 02:04

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DBOTRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.CharField(default=None, max_length=100)),
                ('manager', models.CharField(default=None, max_length=100)),
                ('title', models.CharField(default=None, max_length=100)),
                ('description', models.TextField(default=None)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.DateTimeField(default=None)),
                ('end_time', models.DateTimeField(default=None)),
                ('approved', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'DBOTRequest',
            },
        ),
        migrations.CreateModel(
            name='UserS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=128)),
                ('name', models.CharField(default=None, max_length=128)),
                ('password', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('department', models.CharField(default=None, max_length=255)),
            ],
            options={
                'db_table': 'Employee',
            },
            managers=[
                ('object', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddIndex(
            model_name='users',
            index=models.Index(fields=['email'], name='email_index'),
        ),
    ]
