# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upp_app', '0002_auto_20151129_1543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='code_link',
        ),
    ]
