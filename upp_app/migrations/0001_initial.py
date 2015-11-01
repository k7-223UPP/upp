# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('rating', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('datalink', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TaskInSection',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('id_section', models.ForeignKey(to='upp_app.Section')),
                ('id_task', models.ForeignKey(to='upp_app.Task')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=65)),
                ('nickname', models.CharField(max_length=50)),
            ],
        ),
    ]
