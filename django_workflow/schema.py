import django_filters
from django_workflow import models
from graphene import AbstractType, Node, Field
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField


# State

class StateNode(DjangoObjectType):
    class Meta:
        model = models.State
        interfaces = (Node,)
        filter_fields = ["workflow__id", "workflow__name"]


class StateFilter(django_filters.FilterSet):
    workflow__id = django_filters.ModelChoiceFilter(queryset=models.Workflow.objects.all().values_list('id', flat=True))

    class Meta:
        model = models.State
        fields = {
            "workflow__id": ["exact",],
            "workflow__name": ["exact",],
        }


# State Variable Definition

class StateVariableDefNode(DjangoObjectType):
    class Meta:
        model = models.StateVariableDef
        interfaces = (Node,)
        filter_fields = ["workflow__id", "workflow__name", "state__id", "state__name"]


class StateVariableDefFilter(django_filters.FilterSet):
    workflow__id = django_filters.ModelChoiceFilter(queryset=models.Workflow.objects.all().values_list('id', flat=True))
    state__id = django_filters.ModelChoiceFilter(queryset=models.State.objects.all().values_list('id', flat=True))

    class Meta:
        model = models.StateVariableDef
        fields = {
            "workflow__id": ["exact",],
            "workflow__name": ["exact",],
            "state__id": ["exact", ],
            "state__name": ["exact", ],

        }


# Transition

class TransitionNode(DjangoObjectType):
    class Meta:
        model = models.Transition
        interfaces = (Node,)
        filter_fields = [
            "workflow__id",
            "workflow__name",
            "initial_state__id",
            "initial_state__name",
            "final_state__id",
            "final_state__name"
        ]


class TransitionFilter(django_filters.FilterSet):
    workflow__id = django_filters.ModelChoiceFilter(queryset=models.Workflow.objects.all().values_list('id', flat=True))
    initial_state__id = django_filters.ModelChoiceFilter(queryset=models.State.objects.all().values_list('id', flat=True))
    final_state__id = django_filters.ModelChoiceFilter(queryset=models.State.objects.all().values_list('id', flat=True))

    class Meta:
        model = models.Transition
        fields = {
            "workflow__id": ["exact",],
            "workflow__name": ["exact",],
            "initial_state__id": ["exact",],
            "initial_state__name": ["exact",],
            "final_state__id": ["exact",],
            "final_state__name": ["exact",]
        }


# Workflow

class WorkflowNode(DjangoObjectType):
    initial_state = Field(StateNode)
    initial_transition = Field(TransitionNode)

    class Meta:
        model = models.Workflow
        interfaces = (Node,)
        filter_fields = []

    def resolve_initial_state(self, info):
        return self.initial_state

    def resolve_initial_transition(self, info):
        return self.initial_transition


class WorkflowFilter(django_filters.FilterSet):
    class Meta:
        model = models.Workflow
        fields = []


# Condition

class ConditionNode(DjangoObjectType):
    class Meta:
        model = models.Condition
        interfaces = (Node,)
        filter_fields = [
            "workflow__id",
            "workflow__name",
            "transition__id",
            "transition__name",
            "parent_condition__id"
        ]


class ConditionFilter(django_filters.FilterSet):
    workflow__id = django_filters.ModelChoiceFilter(queryset=models.Workflow.objects.all().values_list('id', flat=True))
    transition__id = django_filters.ModelChoiceFilter(queryset=models.Transition.objects.all().values_list('id', flat=True))
    parent_condition__id = django_filters.ModelChoiceFilter(queryset=models.Condition.objects.all().values_list('id', flat=True))

    class Meta:
        model = models.Condition
        fields = {
            "workflow__id": ["exact",],
            "workflow__name": ["exact",],
            "transition__id": ["exact",],
            "transition__name": ["exact",],
            "parent_condition__id": ["exact",],
        }


# Function

class FunctionNode(DjangoObjectType):
    class Meta:
        model = models.Function
        interfaces = (Node,)
        filter_fields = [
            "workflow__id",
            "workflow__name",
            "condition__id"
        ]


class FunctionFilter(django_filters.FilterSet):
    workflow__id = django_filters.ModelChoiceFilter(queryset=models.Workflow.objects.all().values_list('id', flat=True))
    condition__id = django_filters.ModelChoiceFilter(queryset=models.Condition.objects.all().values_list('id', flat=True))

    class Meta:
        model = models.Function
        fields = {
            "workflow__id": ["exact",],
            "workflow__name": ["exact",],
            "condition__id": ["exact",],
        }

# FunctionParameter

class FunctionParameterNode(DjangoObjectType):
    class Meta:
        model = models.FunctionParameter
        interfaces = (Node,)
        filter_fields = [
            "workflow__id",
            "workflow__name",
            "function__id"
        ]


class FunctionParameterFilter(django_filters.FilterSet):
    workflow__id = django_filters.ModelChoiceFilter(queryset=models.Workflow.objects.all().values_list('id', flat=True))
    function__id = django_filters.ModelChoiceFilter(queryset=models.Function.objects.all().values_list('id', flat=True))

    class Meta:
        model = models.FunctionParameter
        fields = {
            "workflow__id": ["exact",],
            "workflow__name": ["exact",],
            "function__id": ["exact",],
        }

# Callback

class CallbackNode(DjangoObjectType):
    class Meta:
        model = models.Callback
        interfaces = (Node,)
        filter_fields = [
            "workflow__id",
            "workflow__name",
            "transition__id",
            "transition__name",
        ]


class CallbackFilter(django_filters.FilterSet):
    workflow__id = django_filters.ModelChoiceFilter(queryset=models.Workflow.objects.all().values_list('id', flat=True))
    transition__id = django_filters.ModelChoiceFilter(queryset=models.Transition.objects.all().values_list('id', flat=True))

    class Meta:
        model = models.Callback
        fields = {
            "workflow__id": ["exact",],
            "workflow__name": ["exact",],
            "transition__id": ["exact",],
            "transition__name": ["exact",],
        }

# CallbackParameter

class CallbackParameterNode(DjangoObjectType):
    class Meta:
        model = models.CallbackParameter
        interfaces = (Node,)
        filter_fields = [
            "workflow__id",
            "workflow__name",
            "callback__id"
        ]


class CallbackParameterFilter(django_filters.FilterSet):
    workflow__id = django_filters.ModelChoiceFilter(queryset=models.Workflow.objects.all().values_list('id', flat=True))
    callback__id = django_filters.ModelChoiceFilter(queryset=models.Callback.objects.all().values_list('id', flat=True))

    class Meta:
        model = models.CallbackParameter
        fields = {
            "workflow__id": ["exact",],
            "workflow__name": ["exact",],
            "callback__id": ["exact",],
        }


# CurrentObjectState

class CurrentObjectStateNode(DjangoObjectType):
    class Meta:
        model = models.CurrentObjectState
        interfaces = (Node,)
        filter_fields = [
            "workflow__id",
            "workflow__name",
            "state__id",
            "state__name"
        ]


class CurrentObjectStateFilter(django_filters.FilterSet):
    workflow__id = django_filters.ModelChoiceFilter(queryset=models.Workflow.objects.all().values_list('id', flat=True))
    state__id = django_filters.ModelChoiceFilter(queryset=models.State.objects.all().values_list('id', flat=True))

    class Meta:
        model = models.CurrentObjectState
        fields = {
            "workflow__id": ["exact",],
            "workflow__name": ["exact",],
            "state__id": ["exact",],
            "state__name": ["exact",]
        }


# State Variables

class StateVariableNode(DjangoObjectType):
    class Meta:
        model = models.StateVariable
        interfaces = (Node,)
        filter_fields = [
            "workflow__id",
            "workflow__name",
            "current_object_state__state__id",
            "current_object_state__state__name",
            "current_object_state__id",
            "state_variable_def__id",
            "state_variable_def__name"
        ]


class StateVariableFilter(django_filters.FilterSet):
    workflow__id = django_filters.ModelChoiceFilter(queryset=models.Workflow.objects.all().values_list('id', flat=True))
    current_object_state__state__id = django_filters.ModelChoiceFilter(queryset=models.State.objects.all().values_list('id', flat=True))
    current_object_state__id = django_filters.ModelChoiceFilter(queryset=models.CurrentObjectState.objects.all().values_list('id', flat=True))
    state_variable_def__id = django_filters.ModelChoiceFilter(queryset=models.StateVariableDef.objects.all().values_list('id', flat=True))

    class Meta:
        model = models.StateVariable
        fields = {
            "workflow__id": ["exact", ],
            "workflow__name": ["exact", ],
            "current_object_state__state__id": ["exact", ],
            "current_object_state__state__name": ["exact", ],
            "current_object_state__id": ["exact", ],
            "state_variable_def__id": ["exact", ],
            "state_variable_def__name": ["exact", ],
        }


# TransitionLog

class TransitionLogNode(DjangoObjectType):
    class Meta:
        model = models.TransitionLog
        interfaces = (Node,)
        filter_fields = [
            "workflow__id",
            "workflow__name",
            "transition__id",
            "transition__name"
        ]


class TransitionLogFilter(django_filters.FilterSet):
    workflow__id = django_filters.ModelChoiceFilter(queryset=models.Workflow.objects.all().values_list('id', flat=True))
    transition__id = django_filters.ModelChoiceFilter(queryset=models.Transition.objects.all().values_list('id', flat=True))

    class Meta:
        model = models.TransitionLog
        fields = {
            "workflow__id": ["exact",],
            "workflow__name": ["exact",],
            "transition__id": ["exact",],
            "transition__name": ["exact",]
        }


class Query(object):
    workflow_list = DjangoFilterConnectionField(WorkflowNode, filterset_class=WorkflowFilter)
    state_list = DjangoFilterConnectionField(StateNode, filterset_class=StateFilter)
    state_variable_def_list = DjangoFilterConnectionField(StateVariableDefNode, filterset_class=StateVariableDefFilter)
    transition_list = DjangoFilterConnectionField(TransitionNode, filterset_class=TransitionFilter)
    condition_list = DjangoFilterConnectionField(TransitionNode, filterset_class=TransitionFilter)
    function_list = DjangoFilterConnectionField(FunctionNode, filterset_class=FunctionFilter)
    function_parameter_list = DjangoFilterConnectionField(FunctionParameterNode, filterset_class=FunctionParameterFilter)
    callback_list = DjangoFilterConnectionField(CallbackNode, filterset_class=CallbackFilter)
    callback_parameter_list = DjangoFilterConnectionField(CallbackParameterNode, filterset_class=CallbackParameterFilter)
    current_object_state_list = DjangoFilterConnectionField(CurrentObjectStateNode, filterset_class=CurrentObjectStateFilter)
    state_variable_list = DjangoFilterConnectionField(StateVariableNode, filterset_class=StateVariableFilter)
    transition_log_list = DjangoFilterConnectionField(TransitionLogNode, filterset_class=TransitionLogFilter)

