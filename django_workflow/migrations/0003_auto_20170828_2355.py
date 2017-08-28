# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_workflow', '0002_auto_20170828_2306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workflow',
            name='initial_state',
        ),
        migrations.AddField(
            model_name='state',
            name='initial',
            field=models.BooleanField(default=False, verbose_name='Initial'),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='name',
            field=models.CharField(unique=True, max_length=200, verbose_name='Name'),
        ),
        migrations.AlterUniqueTogether(
            name='state',
            unique_together=set([('name', 'workflow')]),
        ),
        migrations.AlterUniqueTogether(
            name='transition',
            unique_together=set([('name', 'initial_state', 'final_state')]),
        ),
    ]
