import time
from django.test import TestCase

from django.contrib.auth.models import User
from django_workflow import workflow
from django_workflow.models import Workflow, State, Transition, Condition, Function, FunctionParameter


class WorkflowTest(TestCase):

    def setUp(self):
        wf = Workflow.objects.create(name="Test_Workflow", object_type="django.contrib.auth.models.User")
        s1 = State.objects.create(name="state 1", workflow=wf, active=True, initial=True)
        s2 = State.objects.create(name="state 2", workflow=wf, active=True)
        s3 = State.objects.create(name="state 3", workflow=wf, active=True)
        t1 = Transition.objects.create(name="auto_fast", initial_state=s1, final_state=s2, automatic=True, automatic_delay=1.0/24.0/3600.0, priority=2)
        t4 = Transition.objects.create(name="auto_slow", initial_state=s1, final_state=s3, automatic=True,
            automatic_delay=1.0 / 24.0, priority=1)

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
        self.assertEqual(manual[0].initial_state.name, "state 1")
        self.assertEqual(manual[0].final_state.name, "state 3")
        s = workflow.get_object_state("Test_Workflow", user.id)
        self.assertEqual(s.name, "state 1")


    def test_export(self):
        data = workflow.export_workflow("Test_Workflow")
        FunctionParameter.objects.all().delete()
        Function.objects.all().delete()
        Condition.objects.all().delete()
        Transition.objects.all().delete()
        State.objects.all().delete()
        Workflow.objects.all().delete()
        workflow.import_workflow(data)
        self.assertTrue(len(FunctionParameter.objects.all()) == 2)
        self.assertTrue(len(Transition.objects.all()) == 4)
        self.assertTrue(len(FunctionParameter.objects.filter(workflow__name="Test_Workflow")) == 2)

    def test_automatic(self):
        user = User.objects.get(username="admin")
        # print(user)
        wf = workflow.get_workflow("Test_Workflow")
        wf.add_object(user.id, async=False)
        time.sleep(2)
        workflow.execute_automatic_transitions(workflow_name="Test_Workflow")
        s = workflow.get_object_state("Test_Workflow", user.id)
        self.assertEqual(s.name, "state 2")
        manual = workflow.get_available_transitions("Test_Workflow", user, user.id)
        manual[0].execute(user, user.id, async=False, automatic=False)
        s = workflow.get_object_state("Test_Workflow", user.id)
        self.assertEqual(s.name, "state 3")

