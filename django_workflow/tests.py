from django.db import transaction
from django.test import TestCase

from django.contrib.auth.models import User
from django_workflow import workflow
from django_workflow.models import Workflow, State, Transition, Condition, Function, FunctionParameter


class TransitionTest(TestCase):

    def setUp(self):
        wf = Workflow.objects.create(name="Test_Workflow", object_type="django.contrib.auth.models.User")
        s1 = State.objects.create(name="state 1", workflow=wf, active=True, initial=True)
        s2 = State.objects.create(name="state 2", workflow=wf, active=True)
        s3 = State.objects.create(name="state 3", workflow=wf, active=True)
        t1 = Transition.objects.create(initial_state=s1, final_state=s2, automatic=True)
        t2 = Transition.objects.create(initial_state=s1, final_state=s3, automatic=False)
        t3 = Transition.objects.create(initial_state=s2, final_state=s3, automatic=False)
        c1 = Condition.objects.create(condition_type="function", transition=t1)
        f1 = Function.objects.create(
            function_name="object_attribute_value",
            function_module="django_workflow.conditions",
            condition=c1
        )
        p11 = FunctionParameter.objects.create(function=f1, name="attribute_name", value="is_superuser")
        p12 = FunctionParameter.objects.create(function=f1, name="attribute_value", value="True")
        User.objects.create(username="admin", is_superuser=True)

    def test_transition_availability(self):
        user = User.objects.get(username="admin")
        #print(user)
        wf = workflow.get_workflow("Test_Workflow")
        wf.add_object(user.id, async=False)
        manual = workflow.get_available_transitions("Test_Workflow", user, user.id)
        self.assertTrue(len(manual) == 1)
        self.assertEqual(manual[0].initial_state.name, "state 2")
        self.assertEqual(manual[0].final_state.name, "state 3")
        s = workflow.get_object_state("Test_Workflow", user.id)
        self.assertEqual(s.name, "state 2")
        manual[0].execute(user, user.id)
        s = workflow.get_object_state("Test_Workflow", user.id)
        self.assertEqual(s.name, "state 3")

    def test_export(self):
        workflow.export_workflow("Test_Workflow", None)
