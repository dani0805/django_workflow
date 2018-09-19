from pandas._libs import json

from django_workflow.conditions import parse_parameters
from django_workflow.models import CurrentObjectState, Workflow


def all_approvals_collected(*ignored, workflow: Workflow, object_id, user, object_state: CurrentObjectState, **kwargs):
    return not object_state.statevariable_set.filter(value="False").exists()

def is_approver(*ignored, workflow: Workflow, object_id, user, object_state: CurrentObjectState, **kwargs):
    params = parse_parameters(workflow=workflow, object_id=object_id, user=user, object_state=object_state, **kwargs)
    if "user_list" in params:
        user_ids = json.loads(params.pop('user_list'))
        if user.id in user_ids:
            return True
    return False

