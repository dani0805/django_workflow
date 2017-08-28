from django.core import serializers

from django_workflow.models import Workflow, State, CurrentObjectState, Transition


def get_workflow(name):
    return Workflow.objects.get(name=name)


def get_available_transitions(workflow_name, user, object_id):
    return get_object_state(workflow_name, object_id).available_transitions(user, object_id)


def get_object_state(workflow_name, object_id):
    wf = get_workflow(workflow_name)
    if not wf:
        raise ValueError("wokflow {} not found!".format(workflow_name))
    state = CurrentObjectState.objects.get(id=object_id, state__workflow__id=wf.id).state
    if state:
        return state
    else:
        raise ValueError("object_id {} not found in workflow {}!".format(object_id, workflow_name))


def export_workflow(workflow_name, file):
    data = serializers.serialize('json', Workflow.objects.all())
    print(data)
    data = serializers.serialize('json', State.objects.all())
    print(data)
    data = serializers.serialize('json', Transition.objects.all())
    print(data)
