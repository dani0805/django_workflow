from django.core.management import BaseCommand

from django_workflow import workflow

__author__ = 'Daniele Bernardini'


class Command(BaseCommand):
    help = 'trigger automatic transitions in django_workflow'

    def handle(self, *args, **options):
        workflow_name = None
        if len(args) > 0:
            workflow_name = args[0]
        workflow.execute_automatic_transitions(workflow_name=workflow_name)
