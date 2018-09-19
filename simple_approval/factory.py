from pandas._libs import json

from django_workflow.models import Workflow, State, Transition, StateVariableDef, Function, Callback, CallbackParameter, \
    Condition, FunctionParameter


class SimpleApprovalFactory:

    @staticmethod
    def new_approval_workflow(*, name: str, object_model: str, user_model="django.contrib.auth.models.User", approval_steps=1) -> Workflow:
        wf = Workflow.objects.create(name=name)
        # 3 states
        initial_state = State.objects.create(name="New", workflow=wf, initial=True, active=True)
        approved_state = initial_state
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
        submission = Transition.objects.create(name="{} Approve".format(name), initial_state=state, final_state=in_approval_state, automatic=False)


        for i in range(parallel_approvals):
            variable_name = "Approval {} {}".format(name, i)
            parallel_name = "Approve {} {}".format(name, i)

            SimpleApprovalFactory.add_parallel_approval(
                workflow=workflow,
                state=in_approval_state,
                name=parallel_name,
                variable_name=variable_name
            )
        # this automatic transition will be activated once all state variable are positive
        all_approvals_completed = Transition.objects.create(name="All {} Approvals Collected".format(name), initial_state=in_approval_state,
            final_state=approved_state, automatic=True)
        all_approvals_condition = Condition.objects.create(condition_type="function", workflow=workflow, transition=all_approvals_completed)
        function = Function.objects.create(
            workflow=workflow,
            function_name="is_approver",
            function_module="django_workflow.all_approvals_collected",
            condition=all_approvals_condition
        )
        return approved_state

    @staticmethod
    def add_parallel_approval(*, workflow: Workflow, state: State, name: str, variable_name: str):
        # for each parallel approval we create an extended state variable holding a boolean value
        approval_granted = StateVariableDef.objects.create(workflow=workflow, state=state, name=variable_name)
        # for each parallel approval we define a independent transition so we can manage the right to
        # execute them with independent function parameters
        approval = Transition.objects.create(name=name, initial_state=state,
            final_state=state, automatic=False)
        SimpleApprovalFactory.set_approval_condtions(approval, workflow)

        # reject should send the object back to the workflow initial state
        reject = Transition.objects.create(
            name="Reject {}".format(name),
            initial_state=state,
            final_state=workflow.initial_state, automatic=False
        )

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
    def set_approval_condtions(approval, workflow):
        condition = Condition.objects.create(condition_type="function", workflow=workflow, transition=approval)
        function = Function.objects.create(
            workflow=workflow,
            function_name="is_approver",
            function_module="django_workflow.simple_approval",
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

