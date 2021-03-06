# Generated by Django 2.0.1 on 2018-01-17 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_workflow', '0007_auto_20180109_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callback',
            name='transition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='django_workflow.Transition', verbose_name='Transition'),
        ),
        migrations.AlterField(
            model_name='callback',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AlterField(
            model_name='callbackparameter',
            name='callback',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='parameters', to='django_workflow.Callback', verbose_name='Callback'),
        ),
        migrations.AlterField(
            model_name='callbackparameter',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AlterField(
            model_name='condition',
            name='parent_condition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child_conditions', to='django_workflow.Condition', verbose_name='Parent Condition'),
        ),
        migrations.AlterField(
            model_name='condition',
            name='transition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_workflow.Transition', verbose_name='Transition'),
        ),
        migrations.AlterField(
            model_name='condition',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AlterField(
            model_name='currentobjectstate',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='django_workflow.State', verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='currentobjectstate',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AlterField(
            model_name='function',
            name='condition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='django_workflow.Condition', verbose_name='Condition'),
        ),
        migrations.AlterField(
            model_name='function',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AlterField(
            model_name='functionparameter',
            name='function',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='parameters', to='django_workflow.Function', verbose_name='Function'),
        ),
        migrations.AlterField(
            model_name='functionparameter',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AlterField(
            model_name='state',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AlterField(
            model_name='transition',
            name='final_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incoming_transitions', to='django_workflow.State', verbose_name='Final State'),
        ),
        migrations.AlterField(
            model_name='transition',
            name='initial_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outgoing_transitions', to='django_workflow.State', verbose_name='Initial State'),
        ),
        migrations.AlterField(
            model_name='transition',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AlterField(
            model_name='transitionlog',
            name='transition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='django_workflow.Transition', verbose_name='Transition'),
        ),
        migrations.AlterField(
            model_name='transitionlog',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
    ]
