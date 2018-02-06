import graphene
from django.core.exceptions import PermissionDenied
from django_workflow import schema
from django_workflow.models import Workflow


class CreateWorkflow(graphene.ClientIDMutation):
    class Input:
        name = graphene.String()

    workflow = graphene.Field(schema.WorkflowNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        context = info.context
        if not context.user.is_authenticated:
            raise PermissionDenied('User is not logged in.')

        name = input
        workflow = Workflow.objects.create(name=name)

        return workflow

class Mutation(graphene.AbstractType):
    """
    Base end point to define all the other mutations for mis
    """

    # MUTATIONS - DOCUMENTS
    create_workflow = CreateWorkflow.Field()