# Generated by Django 2.0.1 on 2018-04-13 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_workflow', '0010_remove_transitionlog_object_state'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='currentobjectstate',
            index=models.Index(fields=['workflow', 'object_id'], name='django_work_workflo_d6495e_idx'),
        ),
    ]
