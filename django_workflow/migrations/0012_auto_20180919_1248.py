# Generated by Django 2.0.1 on 2018-09-19 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_workflow', '0011_auto_20180413_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='StateVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=4000, verbose_name='Value')),
                ('current_object_state', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='django_workflow.CurrentObjectState', verbose_name='Object State')),
            ],
        ),
        migrations.CreateModel(
            name='StateVariableDef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='state', to='django_workflow.State', verbose_name='State')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='django_workflow.Workflow', verbose_name='Workflow')),
            ],
        ),
        migrations.AddField(
            model_name='statevariable',
            name='state_variable_def',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='django_workflow.StateVariableDef', verbose_name='Variable Definition'),
        ),
        migrations.AddField(
            model_name='statevariable',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='django_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AlterUniqueTogether(
            name='statevariabledef',
            unique_together={('name', 'workflow', 'state')},
        ),
    ]
