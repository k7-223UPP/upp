# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('upp_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('code_link', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TestTask',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('datalink', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TestTaskInSection',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserPickedTask',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Verdict',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('verdict_text', models.CharField(max_length=15)),
                ('id_submission', models.ForeignKey(to='upp_app.Submission')),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='section',
            name='description',
            field=models.CharField(default='', max_length=1500),
        ),
        migrations.AddField(
            model_name='section',
            name='short_description',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='userpickedtask',
            name='id_section',
            field=models.ForeignKey(to='upp_app.Section'),
        ),
        migrations.AddField(
            model_name='userpickedtask',
            name='id_task',
            field=models.ForeignKey(to='upp_app.Task'),
        ),
        migrations.AddField(
            model_name='userpickedtask',
            name='id_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='testtaskinsection',
            name='id_section',
            field=models.ForeignKey(to='upp_app.Section'),
        ),
        migrations.AddField(
            model_name='testtaskinsection',
            name='id_test_task',
            field=models.ForeignKey(to='upp_app.TestTask'),
        ),
        migrations.AddField(
            model_name='submission',
            name='id_section',
            field=models.ForeignKey(to='upp_app.Section'),
        ),
        migrations.AddField(
            model_name='submission',
            name='id_task',
            field=models.ForeignKey(to='upp_app.Task'),
        ),
        migrations.AddField(
            model_name='submission',
            name='id_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
