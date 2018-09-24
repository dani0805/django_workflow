import django_filters
import graphene

from django_workflow import models
from graphene import AbstractType, Node, Field
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField


# State
from django_workflow.graph import Graph


# Workflow
from django_workflow.schema import WorkflowNode
from simple_approval.graph import ApprovalGraph


class ApprovalWorkflowNode(WorkflowNode):
    approval_graph = graphene.JSONString()

    class Meta:
        model = models.Workflow
        interfaces = (Node,)
        filter_fields = ["id", "name"]

    def resolve_approval_graph(self, info):
        return ApprovalGraph(workflow=self).nodes_and_links


class ApprovalWorkflowFilter(django_filters.FilterSet):
    class Meta:
        model = models.Workflow
        fields = {
            "id": ["exact", ],
            "name": ["exact", ],
        }




class Query(object):
    approval_workflow_list = DjangoFilterConnectionField(ApprovalWorkflowNode, filterset_class=ApprovalWorkflowFilter)