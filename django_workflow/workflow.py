from django_workflow.models import Workflow


def get_workflow(name):
    return Workflow.objects.get(name=name)

