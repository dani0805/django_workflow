import time
from snapshottest.django import TestCase

from django.contrib.auth.models import User
from django_workflow import workflow
from django_workflow.graph import Graph
from django_workflow.models import Workflow, State, Transition, Condition, Function, FunctionParameter, \
    CurrentObjectState
from simple_approval.factory import SimpleApprovalFactory
from simple_approval.graph import ApprovalGraph
from graphene.test import Client

from schema import schema
from simple_approval.models import ApprovalGroup
from simple_approval.tests_queries import LIST_WORKFLOW_APPROVAL_GRAPH_GQL


class WorkflowTest(TestCase):

    def setUp(self):

        wf = SimpleApprovalFactory.new_approval_workflow (name="Test_Workflow", object_model="django.contrib.auth.models.User", approval_steps=2)
        graph = ApprovalGraph(workflow=wf)
        self.assertTrue(graph.is_connected())

        #print(State.objects.filter(workflow=wf).values_list("name", flat=True))
        first_approved_state = State.objects.get(workflow=wf, name="Submitted for Step 0 Approval")
        user = User.objects.create(username="admin", is_superuser=True)
        user2 = User.objects.create(username="test2", is_superuser=True)
        for t in Transition.objects.filter(automatic=False, workflow=wf):
            SimpleApprovalFactory.set_users_for_approval(workflow=wf, transition_name=t.name,
                user_ids=[user.id, user2.id])
        SimpleApprovalFactory.insert_approval_step(name="Pre", workflow=wf, state=first_approved_state, parallel_approvals=4)
        approval_pattern = [
            ([user.id, user2.id, max(user2.id, user.id) + 1], None, None),
            ([], user.id, None),
            ([user2.id, max(user2.id, user.id) + 1], None, None),
            ([user.id, user2.id, max(user2.id, user.id) + 1], None, user.id)
        ]
        group_ids = ApprovalGroup.objects.filter(
            transitions__initial_state__incoming_transitions__initial_state=first_approved_state
        ).values_list("id", flat=True).distinct()
        groups = ApprovalGroup.objects.filter(id__in=group_ids)
        i = 0
        #print("checking approval groups", groups)
        for g in groups:
            #print("... group")
            for t in g.transitions.all():
                #print("... transition", t.name)
                SimpleApprovalFactory.set_users_for_approval(workflow=wf, transition_name=t.name,
                    user_ids=approval_pattern[i][0])
                if approval_pattern[i][1]:
                    SimpleApprovalFactory.add_user_to_approval(workflow=wf, transition_name=t.name,
                        user_id=approval_pattern[i][1])
                if approval_pattern[i][2]:
                    SimpleApprovalFactory.remove_user_from_approval(workflow=wf, transition_name=t.name,
                        user_id=approval_pattern[i][2])
                #print(FunctionParameter.objects.filter(
                    #function__condition__parent_condition__transition=t,
                    #workflow=wf,
                    #name="user_ids").values_list("value"))
            i = (i + 1) % len(approval_pattern)

    def test_workflow_transitions_and_states(self):
        wf = workflow.get_workflow("Test_Workflow")
        graph = ApprovalGraph(workflow=wf)
        self.assertTrue(graph.is_connected())
        user = User.objects.get(username="admin")
        user2 = User.objects.get(username="test2")
        wf.add_object(user.id, async=False)
        manual = workflow.get_available_transitions("Test_Workflow", user, user.id)
        self.assertEqual(len(manual), 1)
        self.assertEqual(manual[0].initial_state.name, "New")
        self.assertEqual(manual[0].final_state.name, "Submitted for Step 0 Approval")
        s = workflow.get_object_state("Test_Workflow", user.id)
        self.assertEqual(s.name, "New")
        manual[0].execute(user, user.id)
        s = workflow.get_object_state("Test_Workflow", user.id)
        self.assertEqual(s.name, "Submitted for Pre Approval")
        #print("checking manual approval")
        manual2 = workflow.get_available_transitions("Test_Workflow", user, user.id)
        #print([x.name for x in workflow.get_object_state("Test_Workflow", user.id).outgoing_transitions.all()])
        self.assertEqual(len(manual2), 4)
        for t in manual2:
            if t.name.startswith("Approve"):
                t.execute(user, user.id)
        manual3 = workflow.get_available_transitions("Test_Workflow", user2, user.id)
        for t in manual3:
            if t.name.startswith("Approve"):
                t.execute(user2, user.id)
        self.assertEqual("Submitted for Step 1 Approval", workflow.get_object_state(workflow_name=wf.name, object_id=user.id).name)
        manual4 = workflow.get_available_transitions("Test_Workflow", user2, user.id)
        #print("... about to reject")
        for t in manual4:
            #print("Reject final state", t.final_state.name)
            if t.final_state.name == "New":
                t.execute(user2, user.id)
        self.assertEqual("New", workflow.get_object_state(workflow_name=wf.name, object_id=user.id).name)


    def test_modify_workflow(self):
        wf = workflow.get_workflow("Test_Workflow")
        s = State.objects.get(workflow=wf, name="Submitted for Pre Approval")
        client = Client(schema)
        self.assertMatchSnapshot(client.execute(LIST_WORKFLOW_APPROVAL_GRAPH_GQL,
            variables={"param": "Test_Workflow"}))
        SimpleApprovalFactory.remove_approval_step(workflow=wf, state=s, variable_name="Approval Pre 0")
        graph = ApprovalGraph(workflow=wf)
        self.assertTrue(graph.is_connected())

        self.assertMatchSnapshot(client.execute(LIST_WORKFLOW_APPROVAL_GRAPH_GQL,
            variables={"param": "Test_Workflow"}))
        SimpleApprovalFactory.remove_approval_step(workflow=wf, state=s, remove_all=True)
        graph = ApprovalGraph(workflow=wf)
        self.assertTrue(graph.is_connected())

        self.assertMatchSnapshot(client.execute(LIST_WORKFLOW_APPROVAL_GRAPH_GQL,
            variables={"param": "Test_Workflow"}))

    def test_api(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute(LIST_WORKFLOW_APPROVAL_GRAPH_GQL,
            variables={"param": "Test_Workflow"}))




