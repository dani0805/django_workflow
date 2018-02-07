import graphene
from django_workflow import schema
from django_workflow.models import Workflow


class CreateWorkflow(graphene.ClientIDMutation):
    class Input:
        name = graphene.String()
        initialPrefetch = graphene.String()
        objectType = graphene.String()

    workflow = graphene.Field(schema.WorkflowNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        name = input.get('name')
        initial_prefetch = input.get('initialPrefetch')
        object_type = input.get('objectType')
        workflow = Workflow.objects.create(name=name, initial_prefetch=initial_prefetch, object_type=object_type)

        return CreateWorkflow(workflow=workflow)


class UpdateWorkflow(graphene.ClientIDMutation):
    class Input:
        id = graphene.Int()
        name = graphene.String()
        initialPrefetch = graphene.String()
        objectType = graphene.String()

    workflow = graphene.Field(schema.WorkflowNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        name = input.get('name')
        initial_prefetch = input.get('initialPrefetch')
        object_type = input.get('objectType')
        id = input.get('id')
        workflow = Workflow.objects.get(id=id)
        workflow.name = name
        workflow.initial_prefetch = initial_prefetch
        workflow.object_type = object_type
        workflow.save()
        return CreateWorkflow(workflow=workflow)

class Mutation(graphene.AbstractType):
    """
    Base end point to define all the other mutations for mis
    """

    # MUTATIONS - Workflow
    create_workflow = CreateWorkflow.Field()
    update_workflow = UpdateWorkflow.Field()