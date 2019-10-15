import json

from django_workflow.models import Workflow, State, Transition, StateVariableDef, Function, Callback, \
    CallbackParameter, \
    Condition, FunctionParameter
from simple_approval.models import ApprovalGroup
from simple_approval.graph import ApprovalGraph
import uuid


class SimpleApprovalFactory:

    @staticmethod
    def new_approval_workflow(*, name: str, object_model: str, user_model="django.contrib.auth.models.User",
            approval_steps=1) -> Workflow:
        wf = Workflow.objects.create(name=name, object_type=object_model)
        # 3 states
        initial_state = State.objects.create(name="New", workflow=wf, initial=True, active=True)
        if approval_steps == 0:
            # without approval : New -> Approved -> Archived
            approved_state = State.objects.create(name="Approved", workflow=wf, active=True)
            Transition.objects.create(name="Approve", initial_state=initial_state,
                final_state=approved_state, automatic=False)
            SimpleApprovalFactory.set_published_state(workflow=wf, state=approved_state)
        else:
            approved_state = initial_state
            for i in range(approval_steps):
                approved_state = SimpleApprovalFactory.insert_approval_step(name="Step {}".format(i), workflow=wf,
                    state=approved_state)
            approved_state.name = "Approved {}".format(i)
            approved_state.save()
        SimpleApprovalFactory.set_published_state(workflow=wf, state=approved_state)
        archived_state = State.objects.create(name="Archived", workflow=wf, active=False)
        Transition.objects.create(name="Archive", initial_state=approved_state,
            final_state=archived_state, automatic=False)
        SimpleApprovalFactory.set_archived_state(workflow=wf, state=archived_state)

        return wf

    @staticmethod
    def insert_approval_step(*, name: str, workflow: Workflow, state: State, parallel_approvals=1) -> State:
        # create the final state of this approval step
        approved_state = State.objects.create(name="{} Approved".format(name), workflow=workflow, active=True)
        # remove all outgoing transitions from initial state and attach them to approved state
        for t in state.outgoing_transitions.all():
            t.initial_state = approved_state
            # if the transition was origination from the first state then it was a manual submission,
            # in this case we must change it to automatic
            print(t.final_state.name, SimpleApprovalFactory.is_archived(workflow=workflow, state=t.final_state))
            if not SimpleApprovalFactory.is_archived(workflow=workflow, state=t.final_state):
                t.automatic = True
            t.save()
        # create a middle step that will hold the object until all approvals are granted
        in_approval_state = State.objects.create(name="Submitted for {} Approval".format(name), workflow=workflow,
            active=True)
        # submission goes from the initial state to the in_approval, if is the submission from new
        # then manual, otherwise automatic
        is_not_first = state.incoming_transitions.all().count() > 0
        Transition.objects.create(name="Set In Approval {}".format(name), initial_state=state,
            final_state=in_approval_state, automatic=is_not_first)
        for i in range(parallel_approvals):
            variable_name = "Approval {} {}".format(name, i)
            SimpleApprovalFactory.add_parallel_approval(
                workflow=workflow,
                state=in_approval_state,
                variable_name=variable_name
            )
        # this automatic transition will be activated once all state variable are positive
        all_approvals_completed = Transition.objects.create(name="All {} Approvals Collected".format(name),
            initial_state=in_approval_state,
            final_state=approved_state, automatic=True)
        all_approvals_condition = Condition.objects.create(condition_opt="function", workflow=workflow,
            transition=all_approvals_completed)
        Function.objects.create(
            workflow=workflow,
            function_name="all_approvals_collected",
            function_module="simple_approval.conditions",
            condition=all_approvals_condition
        )
        if SimpleApprovalFactory.is_published(workflow=workflow, state=state):
            SimpleApprovalFactory.set_published_state(workflow=workflow, state=approved_state)
        return approved_state

    @staticmethod
    def set_published_state(*, workflow: Workflow, state: State):
        StateVariableDef.objects.filter(workflow=workflow, name__iexact="approved").delete()
        StateVariableDef.objects.create(workflow=workflow, name="approved", state=state)

    @staticmethod
    def get_published_state(*, workflow: Workflow) -> State:
        return State.objects.get(workflow=workflow, variable_definitions__name__iexact="approved")

    @staticmethod
    def is_published(*, workflow: Workflow, state: State):
        return StateVariableDef.objects.filter(workflow=workflow, name__iexact="approved", state=state).exists()

    @staticmethod
    def set_archived_state(*, workflow: Workflow, state: State):
        StateVariableDef.objects.filter(workflow=workflow, name__iexact="archived").delete()
        StateVariableDef.objects.create(workflow=workflow, name="archived", state=state)

    @staticmethod
    def get_archived_state(*, workflow: Workflow) -> State:
        return State.objects.get(workflow=workflow, variable_definitions__name__iexact="archived")

    @staticmethod
    def is_archived(*, workflow: Workflow, state: State):
        return StateVariableDef.objects.filter(workflow=workflow, name__iexact="archived", state=state).exists()

    @staticmethod
    def remove_approval_step(*, workflow: Workflow, state: State, approve_name=None, variable_name=None,
            remove_all=False):
        if remove_all:
            # we are removing the entire approval, i.e. we grab the state before and the state after merge it in
            # one state
            start_state = state.incoming_transitions.all().first().initial_state
            end_state = state.outgoing_transitions.filter(final_state__initial=False).exclude(final_state=state).first().final_state
            is_not_first = start_state.incoming_transitions.all().count() > 0
            for t in end_state.outgoing_transitions.all():
                # submission goes from the initial state to the in_approval, if is the submission from new
                # then manual, otherwise automatic
                t.automatic = is_not_first
                t.initial_state = start_state
                t.save()
            # and remove everything in between
            for t in end_state.incoming_transitions.all():
                SimpleApprovalFactory.remove_transition(t)
            for t in state.outgoing_transitions.all():
                SimpleApprovalFactory.remove_transition(t)
            for t in state.incoming_transitions.all():
                SimpleApprovalFactory.remove_transition(t)
            for v in end_state.variable_definitions.all():
                v.delete()
            for v in state.variable_definitions.all():
                v.delete()
            if SimpleApprovalFactory.is_published(state=end_state, workflow=workflow):
                SimpleApprovalFactory.set_published_state(state=start_state, workflow=workflow)
            state.delete()
            end_state.delete()
        elif variable_name:
            transition = state.outgoing_transitions.get(final_state=state, callback__parameters__name__iexact="variable_name",
                callback__parameters__value=variable_name)
            variable_def = state.variable_definitions.filter(name=variable_name)
            SimpleApprovalFactory.remove_transition(transition)
            variable_def.delete()
        elif approve_name:
            transition = state.outgoing_transitions.get(final_state=state,
                name=approve_name)
            variable_name = CallbackParameter.objects.get(callback__transition=transition, name__iexact="variable_name").value
            variable_def = state.variable_definitions.filter(name=variable_name)
            SimpleApprovalFactory.remove_transition(transition)
            variable_def.delete()
        else:
            raise ValueError("either approve_name or variable_name is provided or remove_all must be true")
        # check graph integrity and raise error if it is not connected
        graph = ApprovalGraph(workflow=workflow)
        if not graph.is_connected():
            raise Exception("Graph is not connected")

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
    def add_parallel_approval(*, workflow: Workflow, state: State, approve_label: str = 'Approve', reject_label: str = 'Reject',
            variable_name: str):
        # set unique names for the transition
        unique = str(uuid.uuid4()).replace("-", '')
        approve_name = 'Approve-{}-{}'.format(workflow.id, state.id) + unique
        reject_name = 'Reject-{}-{}'.format(workflow.id, state.id) + unique

        # for each parallel approval we create an extended state variable holding a boolean value
        StateVariableDef.objects.create(workflow=workflow, state=state, name=variable_name)
        # for each parallel approval we define a independent transition so we can manage the right to
        # execute them with independent function parameters
        approval = Transition.objects.create(name=approve_name, initial_state=state,
            final_state=state, automatic=False, label=approve_label)
        SimpleApprovalFactory.set_approval_condtions(transition=approval, workflow=workflow)
        # reject should send the object back to the workflow initial state
        reject = Transition.objects.create(
            name=reject_name,
            initial_state=state,
            final_state=workflow.initial_state, automatic=False, label=reject_label
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
        CallbackParameter.objects.create(
            name="variable_name",
            workflow=workflow,
            callback=callback,
            value=variable_name
        )
        group = ApprovalGroup.objects.create()
        group.transitions.add(approval, reject)


    @staticmethod
    def set_approval_condtions(*, transition, workflow):
        condition = Condition.objects.create(condition_opt="and", workflow=workflow, transition=transition)
        condition1 = Condition.objects.create(condition_opt="function", workflow=workflow, parent_condition=condition)
        funct1 = Function.objects.create(
            workflow=workflow,
            function_name="is_approver",
            function_module="simple_approval.conditions",
            condition=condition1
        )
        FunctionParameter.objects.create(
            workflow=workflow,
            function=funct1,
            name="user_ids",
            value=json.dumps([])
        )
        FunctionParameter.objects.create(
            workflow=workflow,
            function=funct1,
            name="roles",
            value=json.dumps([])
        )

        condition2 = Condition.objects.create(condition_opt="function", workflow=workflow, parent_condition=condition)
        funct2 = Function.objects.create(
            workflow=workflow,
            function_name="is_not_approved",
            function_module="simple_approval.conditions",
            condition=condition2
        )


    @staticmethod
    def set_users_for_approval(*, workflow: Workflow, transition_name: str, user_ids: [int]):
        for param in FunctionParameter.objects.filter(
                function__condition__parent_condition__transition__group__transitions__name=transition_name,
                workflow=workflow,
                name="user_ids"):
            #print("updating", param)
            param.value = json.dumps(user_ids)
            param.save()

    @staticmethod
    def add_user_to_approval(*, workflow: Workflow, transition_name: str, user_id: int):
        for param in FunctionParameter.objects.filter(
                function__condition__parent_condition__transition__group__transitions__name=transition_name,
                workflow=workflow,
                name="user_ids"):
            param_value = json.loads(param.value)
            param_value.append(user_id)
            param.value = json.dumps(param_value)
            param.save()

    @staticmethod
    def remove_user_from_approval(*, workflow: Workflow, transition_name: str, user_id: int):
        for param in FunctionParameter.objects.filter(
                function__condition__parent_condition__transition__group__transitions__name=transition_name,
                workflow=workflow,
                name="user_ids"):
            param_value = json.loads(param.value)
            param_value.remove(user_id)
            param.value = json.dumps(param_value)
            param.save()

    @staticmethod
    def change_status_name(state_def_id: int, name: str, state: State):
        state_def = StateVariableDef.objects.get(pk=state_def_id)
        old_name = state_def.name
        state_def.name = name
        state_def.save()
        state.name = name
        state.save()
        variable_name = CallbackParameter.objects.filter(name="variable_name", value=old_name, callback__transition__initial_state_id=state.id).first()
        variable_name.value = name
        variable_name.save()