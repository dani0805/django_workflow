import graphene
from graphene_django.rest_framework.mutation import SerializerMutation
from rest_framework import serializers
# from utils import parse_global_ids
from . import schema
from .utils import parse_global_ids
from django_workflow.models import Workflow, State, StateVariableDef, Transition, Condition, Function, \
    FunctionParameter, Callback, CallbackParameter, CurrentObjectState, TransitionLog, StateVariable


class WorkflowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workflow
        fields = ['id', 'name', 'initial_prefetch', 'object_type']


class WorkflowMutation(SerializerMutation):

    class Meta:
        serializer_class = WorkflowSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


class CloneWorkflow(graphene.ClientIDMutation):
    class Input:
        workflow_id = graphene.String()
        name = graphene.String()

    workflow = graphene.Field(schema.WorkflowNode)

    @classmethod
    @parse_global_ids()
    def mutate_and_get_payload(cls, root, info, **input):
        workflow = Workflow.objects.get(pk=input.get('workflow_id'))
        new_workflow, _, _, _ = workflow.clone(name=input.get('name'))
        return CloneWorkflow(workflow=new_workflow)


class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ['id', 'name', 'workflow', 'active', 'initial']


class StateMutation(SerializerMutation):

    class Meta:
        serializer_class = StateSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


class StateVariableDefSerializer(serializers.ModelSerializer):

    class Meta:
        model = StateVariableDef
        fields = ['id', 'name', 'workflow', 'state']


class StateVariableDefMutation(SerializerMutation):

    class Meta:
        serializer_class = StateVariableDefSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


class TransitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transition
        fields = ['id', 'name', 'workflow', 'initial_state', 'final_state', 'priority', 'automatic', 'automatic_delay']


class TransitionMutation(SerializerMutation):

    class Meta:
        serializer_class = TransitionSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = ['id', 'condition_type', 'workflow', 'parent_condition', 'transition']


class ConditionMutation(SerializerMutation):

    class Meta:
        serializer_class = ConditionSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


class FunctionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Function
        fields = ['id', 'function_name', 'workflow', 'function_module', 'condition']


class FunctionMutation(SerializerMutation):

    class Meta:
        serializer_class = FunctionSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


class FunctionParameterSerializer(serializers.ModelSerializer):

    class Meta:
        model = FunctionParameter
        fields = ['id', 'name', 'workflow', 'function', 'value']


class FunctionParameterMutation(SerializerMutation):

    class Meta:
        serializer_class = FunctionParameterSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


class CallbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Callback
        fields = ['id', 'function_name', 'workflow', 'function_module', 'transition', 'order', 'execute_async']


class CallbackMutation(SerializerMutation):

    class Meta:
        serializer_class = CallbackSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


class CallbackParameterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CallbackParameter
        fields = ['id', 'name', 'workflow', 'callback', 'value']


class CallbackParameterMutation(SerializerMutation):

    class Meta:
        serializer_class = CallbackParameterSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


class CurrentObjectStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrentObjectState
        fields = ['id', 'object_id', 'workflow', 'state', 'updated_ts']


class CurrentObjectStateMutation(SerializerMutation):

    class Meta:
        serializer_class = CurrentObjectStateSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


class TransitionLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransitionLog
        fields = ['id', 'object_id', 'workflow', 'user_id', 'transition', 'completed_ts', 'success', 'error_code', 'error_message']


class TransitionLogMutation(SerializerMutation):

    class Meta:
        serializer_class = TransitionLogSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


class StateVariableSerializer(serializers.ModelSerializer):

    class Meta:
        model = StateVariable
        fields = ['id', 'current_object_state', 'workflow', 'state_variable_def', 'value']


class StateVariableMutation(SerializerMutation):

    class Meta:
        serializer_class = StateVariableSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


class Mutation(graphene.AbstractType):
    """
    Low level CRUD -D API
    """

    workflow_mutation = WorkflowMutation.Field()
    state_mutation = StateMutation.Field()
    state_variable_def_mutation = StateVariableDefMutation.Field()
    transition_mutation = TransitionMutation.Field()
    condition_mutation = ConditionMutation.Field()
    function_mutation = FunctionMutation.Field()
    function_parameter_mutation = FunctionParameterMutation.Field()
    callback_mutation = CallbackMutation.Field()
    callback_parameter_mutation = CallbackParameterMutation.Field()
    current_object_state_mutation = CurrentObjectStateMutation.Field()
    transition_log_mutation = TransitionLogMutation.Field()
    clone_workflow = CloneWorkflow.Field()

    """
    High Level API: execute single transition, execute automatic transitions
    """
    # TODO high level api