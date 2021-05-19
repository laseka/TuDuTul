# Generated by Django 3.0.5 on 2021-05-19 00:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('creator', models.CharField(max_length=127)),
                ('content', models.CharField(max_length=1023)),
                ('creation_date', models.DateField(default=datetime.date.today)),
                ('completion_date', models.DateField()),
                ('priority', models.IntegerField()),
                ('owning_table_id', models.IntegerField()),
                ('is_done', models.BooleanField(default=False)),
                ('repetition', models.CharField(choices=[('W', 'Weekly'), ('M', 'Monthly'), ('Y', 'Yearly'), ('N', 'No repetition')], max_length=1)),
                ('category', models.CharField(choices=[('P', 'Personal'), ('W', 'Work'), ('F', 'Family')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('login', models.CharField(max_length=127, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=127, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('friends_list', models.ManyToManyField(related_name='_user_friends_list_+', to='tudutul.User')),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('is_shared', models.BooleanField(default=False)),
                ('owner', models.CharField(max_length=127)),
                ('shared_with', models.ManyToManyField(to='tudutul.User')),
            ],
        ),
    ]
