import django_filters
import graphene
from django_workflow import workflow, models
from graphene import AbstractType, Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField


def workflow_filter(query, field_name, value):
    if value is not None:
        value = int(value)
        query = query.filter(id=value)
    return query


class WorkflowNode(DjangoObjectType):
    class Meta:
        model = models.Workflow
        interfaces = (Node,)
        filter_fields = []


class WorkflowFilter(django_filters.FilterSet):
    wf_id = django_filters.NumberFilter(method=workflow_filter)

    class Meta:
        model = models.Workflow
        fields = []


class Query(AbstractType):
    workflow_list = DjangoFilterConnectionField(WorkflowNode, filterset_class=WorkflowFilter)


