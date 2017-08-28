# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_workflow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='functionparameter',
            name='function',
            field=models.ForeignKey(related_name='parameters', verbose_name='Function', to='django_workflow.Function'),
        ),
        migrations.AlterField(
            model_name='transitionlog',
            name='object_id',
            field=models.IntegerField(verbose_name='Object Id'),
        ),
        migrations.AlterField(
            model_name='transitionlog',
            name='user_id',
            field=models.IntegerField(null=True, verbose_name='User Id', blank=True),
        ),
    ]
