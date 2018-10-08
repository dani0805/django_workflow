# Generated by Django 2.1.1 on 2018-10-05 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_workflow', '0013_auto_20180925_1334'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovalGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transitions', models.ManyToManyField(related_name='group', to='django_workflow.Transition')),
            ],
        ),
    ]