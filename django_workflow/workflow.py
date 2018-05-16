from django.core import serializers

from django_workflow.models import Workflow, State, CurrentObjectState, Transition, Condition, Function, \
    FunctionParameter, Callback, CallbackParameter, _execute_atomatic_transitions


def get_workflow(name):
    return Workflow.objects.get(name=name)


def get_available_transitions(workflow_name, user, object_id):
    state = get_object_state(workflow_name, object_id)
    wf = get_workflow(workflow_name)
    if state:
        transitions = state.available_transitions(user, object_id)
        if state.is_final_state:
            transitions = transitions + [wf.initial_transition,]
        return transitions
    else:
        return [wf.initial_transition,]


def get_object_state(workflow_name, object_id):
    wf = get_workflow(workflow_name)
    if not wf:
        raise ValueError("wokflow {} not found!".format(workflow_name))
    cos = CurrentObjectState.objects.filter(object_id=object_id, state__workflow__id=wf.id).order_by('-id').first()
    # do not raise exceptions because it rollbacks transactions in django 2 and this is not wished if you are just
    # checking if the object has already a workflow. So return None is not found and let the handling to the caller
    if cos is not None:
        return cos.state
    else:
        return None


def execute_transition(workflow_name, transition_name, user, object_id, async=False):
    state = get_object_state(workflow_name, object_id)
    # silently fail if no state found or action not available
    wf = get_workflow(workflow_name)
    transition = wf.trasition_by_name(transition_name)
    if transition and transition.is_available(user, object_id):
        transition.execute(user, object_id)


def is_transition_available(workflow_name, transition_name, user, object_id):
    return len(list(filter(lambda x: x.name == transition_name,
        get_available_transitions(workflow_name, user, object_id)))) == 1


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


def execute_automatic_transitions(workflow_name=None, object_state_id=None, object_id=None):
    # exectute initials
    wfs = Workflow.objects.all()
    if workflow_name:
        wfs = wfs.filter(name=workflow_name)
    for wf in wfs:
        if wf.initial_prefetch:
            objs = wf.prefetch_initial_objects()
            for obj in objs:
                if wf.is_initial_transition_available(None, obj.id, automatic=True):
                    wf.initial_transition.execute(None, obj.id, object_state_id, automatic=True)
    # execute all other automatic trasitions
    objects = CurrentObjectState.objects.filter(state__active=True)
    if workflow_name:
        objects = objects.filter(workflow__name=workflow_name)
        if object_id:
            objects = objects.filter(object_id=object_id)
    if object_id and not workflow_name:
        raise ValueError("object_id cannot be passed without workflow_name")
    for o in objects:
        _execute_atomatic_transitions(o.state, o.object_id, object_state_id, async=False)
