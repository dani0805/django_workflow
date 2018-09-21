import graphene

import django_workflow.schema
import django_workflow.mutation


class Query(django_workflow.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(django_workflow.mutation.Mutation, graphene.ObjectType):
    # This class will inherit from multiple Mutations
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query,  mutation=Mutation)