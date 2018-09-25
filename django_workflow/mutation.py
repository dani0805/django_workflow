import graphene
from graphene_django.rest_framework.mutation import SerializerMutation
from rest_framework import serializers

from django_workflow.models import Workflow, State


class WorkflowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workflow
        fields = ['id', 'name', 'initial_prefetch', 'object_type']


class WorkflowMutation(SerializerMutation):

    class Meta:
        serializer_class = WorkflowSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ['id', 'name', 'workflow', 'active', 'initial']


class StateMutation(SerializerMutation):

    class Meta:
        serializer_class = StateSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'



class Mutation(graphene.AbstractType):
    """
    Base end point to define all the other mutations for mis
    """

    # MUTATIONS - Workflow
    workflow_mutation = WorkflowMutation.Field()
    state_mutation = StateMutation.Field()
