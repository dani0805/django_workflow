from django_workflow.conditions import parse_parameters
from django_workflow.models import Workflow, CurrentObjectState


def on_approval(*ignored, workflow: Workflow, object_id, user, object_state: CurrentObjectState, **kwargs):
    params = parse_parameters(workflow=workflow, object_id=object_id, user=user, object_state=object_state, **kwargs)
    variable_name = params.pop("variable_name")
    object_state.statevariable_set.update(**{variable_name: "True"})
