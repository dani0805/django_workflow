import json

from django_workflow.conditions import parse_parameters
from django_workflow.models import CurrentObjectState, Workflow, Transition, CallbackParameter


def all_approvals_collected(*ignored, workflow: Workflow, object_id: int, user, object_state: CurrentObjectState, **kwargs):
    # approval transitions are those starting and ending on the current state which have an approval
    # variable "variable_name" set in a callback parameter. We use this information to get the list of variable_name's
    variable_names = CallbackParameter.objects.filter(
        workflow=workflow,
        callback__transition__initial_state=object_state.state,
        callback__transition__final_state=object_state.state,
        name="variable_name"
    ).values_list("value", flat=True)

    approvals = object_state.statevariable_set.filter(value="True", state_variable_def__name__in=variable_names)
    return len(approvals) == len(variable_names)

def is_approver(*ignored, workflow: Workflow, object_id, user, object_state: CurrentObjectState, **kwargs):
    params = parse_parameters(workflow=workflow, object_id=object_id, user=user, object_state=object_state, **kwargs)
    if "user_ids" in params:
        user_ids = params.pop('user_ids')
        #print(user_ids, user.id)
        if user and user.id in user_ids:
            return True
    return False

#TODO implement!!!
def is_not_approved(*ignored, workflow: Workflow, object_id, user, object_state: CurrentObjectState, transition: Transition, **kwargs):
    variable_names = CallbackParameter.objects.filter(
        workflow=workflow,
        callback__transition__initial_state=object_state.state,
        callback__transition__final_state=object_state.state,
        callback__transition__group__transitions=transition,
        name="variable_name"
    ).values_list("value", flat=True)
    #print(variable_names)
    approvals = object_state.statevariable_set.filter(state_variable_def__name__in=variable_names)
    #print(approvals, len(approvals) == 0)
    return len(approvals) == 0

