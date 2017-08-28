from django_workflow.models import Workflow, State


def get_workflow(name):
    return Workflow.objects.get(name=name)


def get_available_transitions(workflow_name, user, object_id):
    wf = get_workflow(workflow_name)
    if not wf:
        raise ValueError("wokflow {} not found!".format(workflow_name))
    state = State.objects.filter(object_id=object_id, workflow=wf)
    if state:
        return state.available_transitions(user, object_id)
    else:
        raise ValueError("object_id {} not found in workflow {}!".format(object_id, workflow_name))
