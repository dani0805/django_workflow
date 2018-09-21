# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.db.models import PROTECT


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Callback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('function_name', models.CharField(max_length=200, verbose_name='Name')),
                ('function_module', models.CharField(max_length=400, verbose_name='Module')),
                ('order', models.IntegerField(verbose_name='Order')),
                ('execute_async', models.BooleanField(default=False, verbose_name='Execute Asynchronously')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='CallbackParameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('value', models.CharField(max_length=4000, verbose_name='Value')),
                ('callback', models.ForeignKey(verbose_name='Callback', on_delete=PROTECT, to='django_workflow.Callback')),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('condition_type', models.CharField(max_length=10, verbose_name='Type', choices=[(b'function', b'Function Call'), (b'and', b'Boolean AND'), (b'or', b'Boolean OR'), (b'not', b'Boolean NOT')])),
                ('parent_condition', models.ForeignKey(related_name='child_conditions', on_delete=PROTECT, verbose_name='Parent Condition', blank=True, to='django_workflow.Condition', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentObjectState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.CharField(max_length=200, verbose_name='Object Id')),
                ('updated_ts', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
            ],
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('function_name', models.CharField(max_length=200, verbose_name='Function')),
                ('function_module', models.CharField(max_length=400, verbose_name='Module')),
                ('condition', models.ForeignKey(verbose_name='Condition', on_delete=PROTECT, to='django_workflow.Condition')),
            ],
        ),
        migrations.CreateModel(
            name='FunctionParameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('value', models.CharField(max_length=4000, verbose_name='Value')),
                ('function', models.ForeignKey(related_name='parameters', on_delete=PROTECT, verbose_name='Function', to='django_workflow.Function')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('active', models.BooleanField(verbose_name='Active')),
                ('initial', models.BooleanField(default=False, verbose_name='Initial')),
            ],
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Name', blank=True)),
                ('priority', models.IntegerField(null=True, verbose_name='Priority', blank=True)),
                ('automatic', models.BooleanField(verbose_name='Automatic')),
                ('automatic_delay', models.FloatField(null=True, verbose_name='Automatic Delay in Days', blank=True)),
                ('final_state', models.ForeignKey(related_name='incoming_transitions', on_delete=PROTECT, verbose_name='Final State', to='django_workflow.State')),
                ('initial_state', models.ForeignKey(related_name='outgoing_transitions', on_delete=PROTECT, verbose_name='Initial State', to='django_workflow.State')),
            ],
            options={
                'ordering': ['priority'],
            },
        ),
        migrations.CreateModel(
            name='TransitionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField(null=True, verbose_name='User Id', blank=True)),
                ('object_id', models.IntegerField(verbose_name='Object Id')),
                ('completed_ts', models.DateTimeField(auto_now=True, verbose_name='Time of Completion')),
                ('success', models.BooleanField(verbose_name='Success')),
                ('error_code', models.CharField(blank=True, max_length=5, null=True, verbose_name='Error Code', choices=[(b'400', b'400 - Not Authorized'), (b'500', b'500 - Internal Error')])),
                ('error_message', models.CharField(max_length=4000, null=True, verbose_name='Error Message', blank=True)),
                ('transition', models.ForeignKey(verbose_name='Transition', on_delete=PROTECT, to='django_workflow.Transition')),
            ],
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200, verbose_name='Name')),
                ('object_type', models.CharField(max_length=200, verbose_name='Object_Type')),
            ],
        ),
        migrations.AddField(
            model_name='transitionlog',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AddField(
            model_name='transition',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AddField(
            model_name='state',
            name='workflow',
            field=models.ForeignKey(verbose_name='Workflow', on_delete=PROTECT, to='django_workflow.Workflow'),
        ),
        migrations.AddField(
            model_name='functionparameter',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AddField(
            model_name='function',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AddField(
            model_name='currentobjectstate',
            name='state',
            field=models.ForeignKey(verbose_name='State', on_delete=PROTECT, to='django_workflow.State'),
        ),
        migrations.AddField(
            model_name='currentobjectstate',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AddField(
            model_name='condition',
            name='transition',
            field=models.ForeignKey(verbose_name='Transition', on_delete=PROTECT, blank=True, to='django_workflow.Transition', null=True),
        ),
        migrations.AddField(
            model_name='condition',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AddField(
            model_name='callbackparameter',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AddField(
            model_name='callback',
            name='transition',
            field=models.ForeignKey(verbose_name='Transition', on_delete=PROTECT, to='django_workflow.Transition'),
        ),
        migrations.AddField(
            model_name='callback',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AlterUniqueTogether(
            name='transition',
            unique_together=set([('name', 'initial_state', 'final_state')]),
        ),
        migrations.AlterUniqueTogether(
            name='state',
            unique_together=set([('name', 'workflow')]),
        ),
    ]
