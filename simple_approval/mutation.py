import graphene
import json
from django_workflow.models import Workflow, State
from django_workflow.utils import parse_global_ids
from simple_approval import schema
from simple_approval.factory import SimpleApprovalFactory
from graphql_relay import from_global_id


class CreateApprovalWorkflow(graphene.ClientIDMutation):
    class Input:
        name = graphene.String()
        object_type = graphene.String()
        user_model = graphene.String()
        approval_steps = graphene.Int()

    workflow = graphene.Field(schema.ApprovalWorkflowNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, *, name: str, object_type: str, user_model: str, approval_steps: int):
        workflow = SimpleApprovalFactory.new_approval_workflow(name=name,object_model=object_type, user_model=user_model, approval_steps=approval_steps)

        return CreateApprovalWorkflow(workflow=workflow)


class ApprovalWorkflowAddApprovalStep(graphene.ClientIDMutation):
    class Input:
        workflow_id = graphene.String()
        state_id = graphene.String()
        parallel_approvals = graphene.Int()
        name = graphene.String()

    workflow = graphene.Field(schema.ApprovalWorkflowNode)

    @classmethod
    # @parse_global_ids
    def mutate_and_get_payload(cls, root, info, *, workflow_id: str, state_id: str, name: str, parallel_approvals: int = 1):
        workflow_id = from_global_id(workflow_id)[1]
        state_id = from_global_id(state_id)[1]
        workflow = Workflow.objects.get(id=workflow_id)
        state = State.objects.get(id=state_id)
        SimpleApprovalFactory.insert_approval_step(name=name, workflow=workflow, state=state, parallel_approvals=parallel_approvals)
        return ApprovalWorkflowAddApprovalStep(workflow=workflow)


class ApprovalWorkflowAddParallelApproval(graphene.ClientIDMutation):
    class Input:
        workflow_id = graphene.String()
        state_id = graphene.String()
        parallel_approvals = graphene.Int()
        approve_name = graphene.String()
        reject_name = graphene.String()
        variable_name = graphene.String()

    workflow = graphene.Field(schema.ApprovalWorkflowNode)

    @classmethod
    # @parse_global_ids
    def mutate_and_get_payload(cls, root, info, *, workflow_id: str, state_id: str, approve_name: str, reject_name: str, variable_name: str):
        workflow_id = from_global_id(workflow_id)[1]
        state_id = from_global_id(state_id)[1]
        workflow = Workflow.objects.get(id=workflow_id)
        state = State.objects.get(id=state_id)
        SimpleApprovalFactory.add_parallel_approval(workflow=workflow, state=state, approve_name=approve_name, reject_name=reject_name, variable_name=variable_name)
        return ApprovalWorkflowAddParallelApproval(workflow=workflow)


class ApprovalWorkflowRemoveParallelApproval(graphene.ClientIDMutation):
    class Input:
        workflow_id = graphene.String()
        state_id = graphene.String()
        parallel_approvals = graphene.Int()
        approve_name = graphene.String()
        remove_all = graphene.Boolean()
        variable_name = graphene.String()

    workflow = graphene.Field(schema.ApprovalWorkflowNode)

    @classmethod
    # @parse_global_ids
    def mutate_and_get_payload(cls, root, info, *, workflow_id: str, state_id: str, approve_name: str, reject_name: str, variable_name: str, remove_all: bool):
        workflow_id = from_global_id(workflow_id)[1]
        state_id = from_global_id(state_id)[1]
        workflow = Workflow.objects.get(id=workflow_id)
        state = State.objects.get(id=state_id)
        SimpleApprovalFactory.remove_approval_step(workflow=workflow, state=state, approve_name=approve_name, variable_name=variable_name, remove_all=remove_all)
        return ApprovalWorkflowRemoveParallelApproval(workflow=workflow)


class ApprovalWorkflowAddUserToApproval(graphene.ClientIDMutation):
    class Input:
        workflow_id = graphene.String()
        user_id = graphene.String()
        transition_name = graphene.String()

    workflow = graphene.Field(schema.ApprovalWorkflowNode)

    @classmethod
    # @parse_global_ids
    def mutate_and_get_payload(cls, root, info, *, workflow_id: str, user_id: str, transition_name: str):
        workflow_id = from_global_id(workflow_id)[1]
        user_id = from_global_id(user_id)[1]
        workflow = Workflow.objects.get(id=workflow_id)
        SimpleApprovalFactory.add_user_to_approval(workflow=workflow, transition_name=transition_name, user_id=int(user_id))
        return workflow


class ApprovalWorkflowRemoveUserFromApproval(graphene.ClientIDMutation):
    class Input:
        workflow_id = graphene.String()
        user_id = graphene.String()
        transition_name = graphene.String()

    workflow = graphene.Field(schema.ApprovalWorkflowNode)

    @classmethod
    # @parse_global_ids
    def mutate_and_get_payload(cls, root, info, *, workflow_id: str, user_id: str, transition_name: str):
        workflow_id = from_global_id(workflow_id)[1]
        user_id = from_global_id(user_id)[1]
        workflow = Workflow.objects.get(id=workflow_id)
        SimpleApprovalFactory.remove_user_from_approval(workflow=workflow, transition_name=transition_name,
            user_id=int(user_id))
        return workflow


class ApprovalWorkflowSetUsersForApproval(graphene.ClientIDMutation):
    class Input:
        workflow_id = graphene.String()
        user_ids = graphene.String()
        transition_name = graphene.String()

    workflow = graphene.Field(schema.ApprovalWorkflowNode)

    @classmethod
    # @parse_global_ids
    def mutate_and_get_payload(cls, root, info, *, workflow_id: str, user_ids: str, transition_name: str):
        workflow_id = from_global_id(workflow_id)[1]
        user_id_array = [int(from_global_id(user_id)[1]) for user_id in json.loads(user_ids)]
        workflow = Workflow.objects.get(id=workflow_id)
        SimpleApprovalFactory.set_users_for_approval(workflow=workflow, transition_name=transition_name,
            user_ids=user_id_array)
        return workflow


class Mutation(graphene.AbstractType):
    """
    Base end point to define all the other mutations for simple_approval
    """

    # MUTATIONS - ApprovalWorkflow
    create_approval_workflow = CreateApprovalWorkflow.Field()
    approval_workflow_add_approval_step = ApprovalWorkflowAddApprovalStep.Field()
    approval_workflow_add_parallel_approval = ApprovalWorkflowAddParallelApproval.Field()
    approval_workflow_remove_parallel_approval = ApprovalWorkflowRemoveParallelApproval.Field()
