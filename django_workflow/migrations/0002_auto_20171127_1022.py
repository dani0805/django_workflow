# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-27 10:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_workflow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callbackparameter',
            name='callback',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameters', to='django_workflow.Callback', verbose_name='Callback'),
        ),
        migrations.AlterField(
            model_name='condition',
            name='condition_type',
            field=models.CharField(choices=[('function', 'Function Call'), ('and', 'Boolean AND'), ('or', 'Boolean OR'), ('not', 'Boolean NOT')], max_length=10, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='transitionlog',
            name='error_code',
            field=models.CharField(blank=True, choices=[('400', '400 - Not Authorized'), ('500', '500 - Internal Error')], max_length=5, null=True, verbose_name='Error Code'),
        ),
    ]
