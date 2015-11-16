# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upp_app', '0003_section_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='short_description',
            field=models.CharField(default='', max_length=255),
        ),
    ]
