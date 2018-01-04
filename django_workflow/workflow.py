from django.core import serializers

from django_workflow.models import Workflow, State, CurrentObjectState, Transition, Condition, Function, \
    FunctionParameter, Callback, CallbackParameter, _execute_atomatic_transitions


def get_workflow(name):
    return Workflow.objects.get(name=name)


def get_available_transitions(workflow_name, user, object_id):
    return get_object_state(workflow_name, object_id).available_transitions(user, object_id)


def get_object_state(workflow_name, object_id):
    wf = get_workflow(workflow_name)
    if not wf:
        raise ValueError("wokflow {} not found!".format(workflow_name))
    state = CurrentObjectState.objects.get(object_id=object_id, state__workflow__id=wf.id).state
    if state:
        return state
    else:
        raise ValueError("object_id {} not found in workflow {}!".format(object_id, workflow_name))


def is_object_in_workflow(workflow_name, object_id):
    return CurrentObjectState.objects.filter(object_id=object_id, workflow__name=workflow_name).exists()


def export_workflow(workflow_name):
    objects = Workflow.objects.all()
    if workflow_name:
        objects = Workflow.objects.filter(name=workflow_name)

    data = serializers.serialize('json',
                                 list(objects)
                                 + list(State.objects.filter(workflow__in=objects))
                                 + list(Transition.objects.filter(workflow__in=objects))
                                 + list(Condition.objects.filter(workflow__in=objects))
                                 + list(Function.objects.filter(workflow__in=objects))
                                 + list(FunctionParameter.objects.filter(workflow__in=objects))
                                 + list(Callback.objects.filter(workflow__in=objects))
                                 + list(CallbackParameter.objects.filter(workflow__in=objects)),
                                 indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return data


def import_workflow(data):
    for deserialized_object in serializers.deserialize("json", data):
        deserialized_object.save()


def execute_automatic_transitions(workflow_name=None, object_id=None):
    #exectute initials
    wfs = Workflow.objects.all()
    if workflow_name:
        wfs = wfs.filter(name=workflow_name)
    for wf in wfs:
        objs = wf.prefetch_initial_objects()
        for obj in objs:
            if wf.is_initial_transition_available(None, obj.id, automatic=True):
                wf.initial_transition.execute(None, obj.id, automatic=True)
    #execute all other automatic trasitions
    objects = CurrentObjectState.objects.filter(state__active=True)
    if workflow_name:
        objects = objects.filter(workflow__name=workflow_name)
        if object_id:
            objects = objects.filter(object_id=object_id)
    if object_id and not workflow_name:
        raise ValueError("object_id cannot be passed without workflow_name")
    for o in objects:
        _execute_atomatic_transitions(o.state, o.object_id, async=False)


