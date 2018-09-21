from django_workflow.conditions import parse_parameters
from django_workflow.models import Workflow, CurrentObjectState, StateVariableDef


def on_approval(*ignored, workflow: Workflow, object_id, user, object_state: CurrentObjectState, **kwargs):
    params = parse_parameters(workflow=workflow, object_id=object_id, user=user, object_state=object_state, **kwargs)
    variable_name = params.pop("variable_name")
    variable_def = StateVariableDef.objects.get(workflow=workflow, name=variable_name)
    variable, _ = object_state.statevariable_set.get_or_create(workflow=workflow, state_variable_def=variable_def)
    variable.value = "True"
    variable.save()
