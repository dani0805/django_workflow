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
from simple_approval.tests_queries import LIST_WORKFLOW_APPROVAL_GRAPH_GQL


class WorkflowTest(TestCase):

    def setUp(self):

        wf = SimpleApprovalFactory.new_approval_workflow (name="Test_Workflow", object_model="django.contrib.auth.models.User", approval_steps=2)
        first_approved_state = State.objects.get(workflow=wf, name="Submitted")
        user = User.objects.create(username="admin", is_superuser=True)
        user2 = User.objects.create(username="test2", is_superuser=True)
        SimpleApprovalFactory.insert_approval_step(name="Pre", workflow=wf, state=first_approved_state, parallel_approvals=4)
        SimpleApprovalFactory.set_users_for_approval(workflow=wf, transition_name="Approve Pre 0", user_ids=[user.id, user2.id, max(user2.id, user.id) + 1])
        SimpleApprovalFactory.add_user_to_approval(workflow=wf, transition_name="Approve Pre 1", user_id=user.id)
        SimpleApprovalFactory.set_users_for_approval(workflow=wf, transition_name="Approve Pre 2", user_ids=[user2.id, max(user2.id, user.id) + 1])
        SimpleApprovalFactory.set_users_for_approval(workflow=wf, transition_name="Approve Pre 3", user_ids=[user.id, user2.id, max(user2.id, user.id) + 1])
        SimpleApprovalFactory.remove_user_from_approval(workflow=wf, transition_name="Approve Pre 3", user_id=user.id)
        SimpleApprovalFactory.set_users_for_approval(workflow=wf, transition_name="Reject Pre 0", user_ids=[user.id, user2.id, max(user2.id, user.id) + 1])
        SimpleApprovalFactory.add_user_to_approval(workflow=wf, transition_name="Reject Pre 1", user_id=user.id)
        SimpleApprovalFactory.set_users_for_approval(workflow=wf, transition_name="Reject Pre 2", user_ids=[user2.id, max(user2.id, user.id) + 1])
        SimpleApprovalFactory.set_users_for_approval(workflow=wf, transition_name="Reject Pre 3", user_ids=[user.id, user2.id, max(user2.id, user.id) + 1])
        SimpleApprovalFactory.remove_user_from_approval(workflow=wf, transition_name="Reject Pre 3", user_id=user.id)


    def test_workflow_transitions_and_states(self):
        user = User.objects.get(username="admin")
        user2 = User.objects.get(username="test2")
        wf = workflow.get_workflow("Test_Workflow")
        wf.add_object(user.id, async=False)
        manual = workflow.get_available_transitions("Test_Workflow", user, user.id)
        self.assertEqual(len(manual), 1)
        self.assertEqual(manual[0].initial_state.name, "New")
        self.assertEqual(manual[0].final_state.name, "Submitted")
        s = workflow.get_object_state("Test_Workflow", user.id)
        self.assertEqual(s.name, "New")
        print("testing {}".format(manual[0].name))
        manual[0].execute(user, user.id)
        s = workflow.get_object_state("Test_Workflow", user.id)
        self.assertEqual(s.name, "Submitted for Pre Approval")
        manual2 = workflow.get_available_transitions("Test_Workflow", user, user.id)
        self.assertEqual(len(manual2), 4)
        for t in manual2:
            if t.name.startswith("Approve"):
                t.execute(user, user.id)
        manual3 = workflow.get_available_transitions("Test_Workflow", user2, user.id)
        for t in manual3:
            if t.name.startswith("Approve"):
                t.execute(user2, user.id)
        self.assertEqual("Submitted for Step 0 Approval", workflow.get_object_state(workflow_name=wf.name, object_id=user.id).name)

    def test_api(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute(LIST_WORKFLOW_APPROVAL_GRAPH_GQL,
            variables={"param": "Test_Workflow"}))




