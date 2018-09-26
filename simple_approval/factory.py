import json

from django_workflow.models import Workflow, State, Transition, StateVariableDef, Function, Callback, CallbackParameter, \
    Condition, FunctionParameter


class SimpleApprovalFactory:

    @staticmethod
    def new_approval_workflow(*, name: str, object_model: str, user_model="django.contrib.auth.models.User", approval_steps=1) -> Workflow:
        wf = Workflow.objects.create(name=name)
        # 3 states
        initial_state = State.objects.create(name="New", workflow=wf, initial=True, active=True)
        submitted_state = State.objects.create(name="Submitted", workflow=wf, active=True)
        submission = Transition.objects.create(name="Submit for Approval", initial_state=initial_state,
            final_state=submitted_state, automatic=False)
        approved_state = submitted_state
        for i in range(approval_steps):
            approved_state = SimpleApprovalFactory.insert_approval_step(name="Step {}".format(i), workflow=wf, state=approved_state)
        approved_state.active = False
        approved_state.save()
        return wf

    @staticmethod
    def insert_approval_step(*, name:str, workflow: Workflow, state: State, parallel_approvals=1) -> State:
        # create the final state of this approval step
        approved_state = State.objects.create(name="{} Approved".format(name), workflow=workflow, active=True)
        # remove all outgoing transitions from initial state and attach them to approved state
        for t in state.outgoing_transitions.all():
            t.initial_state = approved_state
            t.save()
        # create a middle step that will hold the object until all approvals are granted
        in_approval_state = State.objects.create(name="Submitted for {} Approval".format(name), workflow=workflow, active=True)
        # submission goes from the initial state to the in_approval
        submission = Transition.objects.create(name="Set In Approval {}".format(name), initial_state=state, final_state=in_approval_state, automatic=True)
        for i in range(parallel_approvals):
            variable_name = "Approval {} {}".format(name, i)
            parallel_approval_name = "Approve {} {}".format(name, i)
            parallel_rejection_name = "Reject {} {}".format(name, i)
            SimpleApprovalFactory.add_parallel_approval(
                workflow=workflow,
                state=in_approval_state,
                approve_name=parallel_approval_name,
                reject_name=parallel_rejection_name,
                variable_name=variable_name
            )
        # this automatic transition will be activated once all state variable are positive
        all_approvals_completed = Transition.objects.create(name="All {} Approvals Collected".format(name), initial_state=in_approval_state,
            final_state=approved_state, automatic=True)
        all_approvals_condition = Condition.objects.create(condition_type="function", workflow=workflow, transition=all_approvals_completed)
        function = Function.objects.create(
            workflow=workflow,
            function_name="all_approvals_collected",
            function_module="simple_approval.conditions",
            condition=all_approvals_condition
        )
        return approved_state

    @staticmethod
    def remove_approval_step(*, workflow: Workflow, state: State, approve_name=None, variable_name=None, remove_all=False):
        if remove_all:
            # we are removing the entire approval, i.e. we grab the state before and the state after merge it in
            # one state
            start_state: State = state.incoming_transitions.all().first().initial_state
            end_state: State = state.outgoing_transitions.filter(final_state__initial=False).first().final_state
            for t in end_state.outgoing_transitions.all():
                t.initial_state = start_state
                t.save()
            # and remove everything in between
            for t in end_state.incoming_transitions.all():
                SimpleApprovalFactory.remove_transition(t)
            for t in state.outgoing_transitions.all():
                SimpleApprovalFactory.remove_transition(t)
            for t in state.incoming_transitions.all():
                SimpleApprovalFactory.remove_transition(t)
            for v in state.variable_definitions.all():
                v.delete()
            state.delete()
            end_state.delete()
        elif variable_name:
            transition = state.outgoing_transitions.get(final_state=state, callback__parameters__name="variable_name", callback__parameters__value=variable_name)
            variable_def = state.variable_definitions.filter(name=variable_name)
            SimpleApprovalFactory.remove_transition(transition)
            variable_def.delete()
        elif approve_name:
            transition = state.outgoing_transitions.get(final_state=state,
                name=approve_name)
            variable_name= CallbackParameter.objects.get(callback__transition=transition, name="variable_name").value
            variable_def = state.variable_definitions.filter(name=variable_name)
            SimpleApprovalFactory.remove_transition(transition)
            variable_def.delete()
        else:
            raise ValueError("either approve_name or variable_name is provided or remove_all must be true")

    @staticmethod
    def remove_transition(transition: Transition):
        for c in transition.condition_set.all():
            SimpleApprovalFactory.remove_condition(c)
        for k in transition.callback_set.all():
            for p in k.parameters.all():
                p.delete()
            k.delete()
        transition.delete()

    @staticmethod
    def remove_condition(condition: Condition):
        for c in condition.child_conditions.all():
            SimpleApprovalFactory.remove_condition(c)
        for f in condition.function_set.all():
            for p in f.parameters.all():
                p.delete()
            f.delete()
        condition.delete()


    @staticmethod
    def add_parallel_approval(*, workflow: Workflow, state: State, approve_name: str, reject_name: str, variable_name: str):
        # for each parallel approval we create an extended state variable holding a boolean value
        approval_granted = StateVariableDef.objects.create(workflow=workflow, state=state, name=variable_name)
        # for each parallel approval we define a independent transition so we can manage the right to
        # execute them with independent function parameters
        approval = Transition.objects.create(name=approve_name, initial_state=state,
            final_state=state, automatic=False)
        SimpleApprovalFactory.set_approval_condtions(transition=approval, workflow=workflow)
        # reject should send the object back to the workflow initial state
        reject = Transition.objects.create(
            name=reject_name,
            initial_state=state,
            final_state=workflow.initial_state, automatic=False
        )
        SimpleApprovalFactory.set_approval_condtions(transition=reject, workflow=workflow)
        # on approval we update the state variable as positive
        callback = Callback.objects.create(
            function_name="on_approval",
            function_module="simple_approval.callbacks",
            workflow=workflow,
            transition=approval,
            order=1,
            execute_async=False
        )
        # this stores the name of the variable to be updated
        param = CallbackParameter.objects.create(
            name="variable_name",
            workflow=workflow,
            callback=callback,
            value=variable_name
        )

    @staticmethod
    def set_approval_condtions(*, transition, workflow):
        condition = Condition.objects.create(condition_type="function", workflow=workflow, transition=transition)
        function = Function.objects.create(
            workflow=workflow,
            function_name="is_approver",
            function_module="simple_approval.conditions",
            condition=condition
        )
        function_parameter_ids = FunctionParameter.objects.create(
            workflow=workflow,
            function=function,
            name="user_ids",
            value=json.dumps([])
        )
        function_parameter_roles = FunctionParameter.objects.create(
            workflow=workflow,
            function=function,
            name="roles",
            value=json.dumps([])
        )

    @staticmethod
    def set_users_for_approval(*, workflow:Workflow, transition_name:str, user_ids:[int]):
        param = FunctionParameter.objects.get(function__condition__transition__name=transition_name, workflow=workflow, name="user_ids")
        param_value = json.loads(param.value)
        param.value = json.dumps(user_ids)
        param.save()

    @staticmethod
    def add_user_to_approval(*, workflow:Workflow, transition_name:str, user_id:int):
        param = FunctionParameter.objects.get(function__condition__transition__name=transition_name, workflow=workflow, name="user_ids")
        param_value = json.loads(param.value)
        param_value.append(user_id)
        param.value = json.dumps(param_value)
        param.save()

    @staticmethod
    def remove_user_from_approval(*, workflow: Workflow, transition_name: str, user_id: int):
        param = FunctionParameter.objects.get(function__condition__transition__name=transition_name, workflow=workflow, name="user_ids")
        param_value = json.loads(param.value)
        param_value.remove(user_id)
        param.value = json.dumps(param_value)
        param.save()

