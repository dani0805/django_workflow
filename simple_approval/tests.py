import time
from django.test import TestCase

from django.contrib.auth.models import User
from django_workflow import workflow
from django_workflow.models import Workflow, State, Transition, Condition, Function, FunctionParameter
from simple_approval.factory import SimpleApprovalFactory


class WorkflowTest(TestCase):

    def setUp(self):

        wf = SimpleApprovalFactory.new_approval_workflow (name="Test_Workflow", object_model="django.contrib.auth.models.User", approval_steps=2)
        first_approved_state = State.objects.get(workflow=wf, name="Step 1 Approved")
        SimpleApprovalFactory.insert_approval_step(name="Pre", workflow=wf, state=first_approved_state, parallel_approvals=4)
        User.objects.create(username="admin", is_superuser=True)

    def test_transition_availability(self):
        user = User.objects.get(username="admin")
        wf = workflow.get_workflow("Test_Workflow")
        wf.add_object(user.id, async=False)
        manual = workflow.get_available_transitions("Test_Workflow", user, user.id)
        self.assertTrue(len(manual) == 1)
        #self.assertEqual(manual[0].initial_state.name, "state 1")
        #self.assertEqual(manual[0].final_state.name, "state 3")
        #s = workflow.get_object_state("Test_Workflow", user.id)
        #self.assertEqual(s.name, "state 1")
