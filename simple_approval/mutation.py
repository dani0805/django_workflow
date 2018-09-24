import graphene
from django_workflow.models import Workflow, State
from django_workflow.utils import parse_global_ids
from simple_approval import schema
from simple_approval.factory import SimpleApprovalFactory


class CreateApprovalWorkflow(graphene.ClientIDMutation):
    class Input:
        name = graphene.String()
        objectType = graphene.String()
        userModel = graphene.String()
        approvalSteps = graphene.Int()

    workflow = graphene.Field(schema.ApprovalWorkflowNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, *, name: str, objectType: str, userModel: str, approvalSteps: int):
        workflow = SimpleApprovalFactory.new_approval_workflow(name=name,object_model=objectType, user_model=userModel, approval_steps=approvalSteps)

        return CreateApprovalWorkflow(workflow=workflow)


class ApprovalWorkflowAddApprovalStep(graphene.ClientIDMutation):
    class Input:
        workflow_id = graphene.Int()
        state_id = graphene.Int()
        parallel_approvals = graphene.Int()
        name = graphene.String()

    workflow = graphene.Field(schema.ApprovalWorkflowNode)

    @classmethod
    @parse_global_ids
    def mutate_and_get_payload(cls, root, info, *, workflow_id: str, state_id: str, name: str, parallel_approvals: int = 1):
        workflow = Workflow.objects.get(id=workflow_id)
        state = State.objects.get(id=state_id)
        SimpleApprovalFactory.insert_approval_step(name=name, workflow=workflow, state=state, parallel_approvals=parallel_approvals)
        return ApprovalWorkflowAddApprovalStep(workflow=workflow)


class ApprovalWorkflowAddParallelApproval(graphene.ClientIDMutation):
    class Input:
        workflow_id = graphene.Int()
        state_id = graphene.Int()
        parallel_approvals = graphene.Int()
        approve_name = graphene.String()
        reject_name = graphene.String()
        variable_name = graphene.String()

    workflow = graphene.Field(schema.ApprovalWorkflowNode)

    @classmethod
    @parse_global_ids
    def mutate_and_get_payload(cls, root, info, *, workflow_id: str, state_id: str, approve_name: str, reject_name: str, variable_name: str):
        workflow = Workflow.objects.get(id=workflow_id)
        state = State.objects.get(id=state_id)
        SimpleApprovalFactory.add_parallel_approval(workflow=workflow, state=state, approve_name=approve_name, reject_name=reject_name, variable_name=variable_name)
        return ApprovalWorkflowAddParallelApproval(workflow=workflow)


class ApprovalWorkflowRemoveParallelApproval(graphene.ClientIDMutation):
    class Input:
        workflow_id = graphene.Int()
        state_id = graphene.Int()
        parallel_approvals = graphene.Int()
        approve_name = graphene.String()
        remove_all = graphene.Boolean()
        variable_name = graphene.String()

    workflow = graphene.Field(schema.ApprovalWorkflowNode)

    @classmethod
    @parse_global_ids
    def mutate_and_get_payload(cls, root, info, *, workflow_id: str, state_id: str, approve_name: str, reject_name: str, variable_name: str, remove_all: bool):
        workflow = Workflow.objects.get(id=workflow_id)
        state = State.objects.get(id=state_id)
        SimpleApprovalFactory.remove_approval_step(workflow=workflow, state=state, approve_name=approve_name, variable_name=variable_name, remove_all=remove_all)
        return ApprovalWorkflowRemoveParallelApproval(workflow=workflow)


class Mutation(graphene.AbstractType):
    """
    Base end point to define all the other mutations for simple_approval
    """

    # MUTATIONS - ApprovalWorkflow
    create_approval_workflow = CreateApprovalWorkflow.Field()
    approval_workflow_add_approval_step = ApprovalWorkflowAddApprovalStep.Field()
    approval_workflow_add_parallel_approval = ApprovalWorkflowAddParallelApproval.Field()
    approval_workflow_remove_parallel_approval = ApprovalWorkflowRemoveParallelApproval.Field()
