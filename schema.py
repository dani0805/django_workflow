import graphene

import django_workflow.schema
import django_workflow.mutation
import simple_approval.schema


class Query(django_workflow.schema.Query, simple_approval.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(django_workflow.mutation.Mutation, graphene.ObjectType):
    # This class will inherit from multiple Mutations
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query,  mutation=Mutation)