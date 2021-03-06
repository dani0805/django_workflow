import time
#from django.test import TestCase
from django.db.models import Q
from snapshottest.django import TestCase


from django.contrib.auth.models import User
from django_workflow import workflow
from django_workflow.graph import Graph
from django_workflow.tests_queries import LIST_WORKFLOWS_GQL, LIST_STATES_GQL, \
    LIST_TRANSITIONS_GQL, LIST_WORKFLOW_STATES_GQL, LIST_WORKFLOW_GRAPH_GQL, MUTATE_WORKFLOW_GRAPH_GQL, \
    MUTATE_STATE_GRAPH_GQL
from schema import schema
from django_workflow.models import Workflow, State, Transition, Condition, Function, FunctionParameter, Callback, \
    CallbackParameter, TransitionLog, clone
from graphene.test import Client


def _print(workflow, user, object_id, object_state=None, text=""):
    print(text)


def api_client_get(url):
    return {
        'url': url,
    }


class WorkflowTest(TestCase):

    def setUp(self):
        # create the main workflow object
        wf = Workflow.objects.create(
            name="Test_Workflow",
            object_type="django.contrib.auth.models.User",
            initial_prefetch="""
                             {
                                "username":"admin",
                                "date_joined__gte":"today - 24*3600"
                             }
                             """
        )
        # create 3 states
        s1 = State.objects.create(name="state 1", workflow=wf, active=True, initial=True)
        s2 = State.objects.create(name="state 2", workflow=wf, active=True)
        #the final state is defined as inactive so that its skipped when scanning for automatic transitions
        s3 = State.objects.create(name="state 3", workflow=wf, active=False)
        # create the transitions, we have 2 automatic transitions from state 1 to state 2,
        # the first is going to be executed despite t4 having a better priority because
        # t1 has a lower automatic_delay
        t0 = Transition.objects.create(name="auto_initial", final_state=s1, automatic=True)

        t1 = Transition.objects.create(name="auto_fast", initial_state=s1, final_state=s2, automatic=True, automatic_delay=1.0/24.0/3600.0, priority=2)
        t4 = Transition.objects.create(name="auto_slow", initial_state=s1, final_state=s3, automatic=True,
            automatic_delay=1.0 / 24.0, priority=1)
        t2 = Transition.objects.create(name="manual_1", initial_state=s1, final_state=s3, automatic=False)
        # t5 does not change state and has a delay of 1 second so it should be executed only after the wait
        t5 = Transition.objects.create(name="auto_self", initial_state=s2, final_state=s2, automatic=True,
            automatic_delay=1.0 / 24.0 /3600.0, priority=1)

        t3 = Transition.objects.create(name="manual_2", initial_state=s2, final_state=s3, automatic=False)
        # we set t3 to be executed only by superusers this can be done with a object_attribute_value conditon
        c1 = Condition.objects.create(condition_opt="function", transition=t3)
        f1 = Function.objects.create(
            function_name="object_attribute_value",
            function_module="django_workflow.conditions",
            condition=c1
        )
        p11 = FunctionParameter.objects.create(function=f1, name="attribute_name", value="is_superuser")
        p12 = FunctionParameter.objects.create(function=f1, name="attribute_value", value="True")

        c2 = Condition.objects.create(condition_opt="function", transition=t0)
        f2 = Function.objects.create(
            function_name="object_attribute_value",
            function_module="django_workflow.conditions",
            condition=c2
        )
        p21 = FunctionParameter.objects.create(function=f2, name="attribute_name", value="username")
        p22 = FunctionParameter.objects.create(function=f2, name="attribute_value", value="{{ object.username }}")

        # we want to print out if transition 1 was executed, this can be done with a callback
        cb1 = Callback.objects.create(transition=t1, function_name="_print", function_module="django_workflow.tests", order=1)
        cp11 = CallbackParameter.objects.create(callback=cb1, name="text", value="Transition 1 Executed")
        User.objects.create(username="admin", is_superuser=True, id=1)

    def test_transition_availability(self):
        user = User.objects.get(username="admin")
        #print(user)
        #wf = workflow.get_workflow("Test_Workflow")
        workflow.execute_automatic_transitions()
        #wf.add_object(user.id, async=False)
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
        CallbackParameter.objects.all().delete()
        Callback.objects.all().delete()
        TransitionLog.objects.all().delete()
        Transition.objects.all().delete()
        State.objects.all().delete()
        Workflow.objects.all().delete()
        workflow.import_workflow(data)
        self.assertTrue(len(FunctionParameter.objects.all()) == 4)
        self.assertTrue(len(Transition.objects.all()) == 6)
        self.assertTrue(len(FunctionParameter.objects.filter(workflow__name="Test_Workflow")) == 4)

    def test_automatic(self):
        user = User.objects.get(username="admin")
        # print(user)
        #wf = workflow.get_workflow("Test_Workflow")
        #wf.add_object(user.id, async=False)
        workflow.execute_automatic_transitions()
        time.sleep(2)
        workflow.execute_automatic_transitions(workflow_name="Test_Workflow")
        s = workflow.get_object_state("Test_Workflow", user.id)
        self.assertEqual(s.name, "state 2")
        time.sleep(2)
        self.assertEqual(TransitionLog.objects.count(), 2)
        workflow.execute_automatic_transitions(workflow_name="Test_Workflow")
        self.assertEqual(TransitionLog.objects.count(), 3)
        workflow.execute_automatic_transitions(workflow_name="Test_Workflow")
        self.assertEqual(TransitionLog.objects.count(), 3)
        time.sleep(2)
        workflow.execute_automatic_transitions(workflow_name="Test_Workflow")
        self.assertEqual(TransitionLog.objects.count(), 4)
        manual = workflow.get_available_transitions("Test_Workflow", user, user.id)
        #print("manual transitions: {}".format(manual))
        manual[0].execute(user, user.id)
        s = workflow.get_object_state("Test_Workflow", user.id)
        self.assertEqual(s.name, "state 3")

    def test_api(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute(LIST_WORKFLOWS_GQL))
        self.assertMatchSnapshot(client.execute(LIST_STATES_GQL))
        self.assertMatchSnapshot(client.execute(LIST_WORKFLOW_STATES_GQL,
            variables={"param": "V29ya2Zsb3dOb2RlOjE="}))
        self.assertMatchSnapshot(client.execute(LIST_TRANSITIONS_GQL))
        self.assertMatchSnapshot(client.execute(MUTATE_WORKFLOW_GRAPH_GQL,
            variables={"param": {"name": "Test_Workflow 2", "objectType": "django.contrib.auth.User", "initialPrefetch": ""}}))
        self.assertMatchSnapshot(client.execute(MUTATE_WORKFLOW_GRAPH_GQL,
            variables={
                "param": {"name": "Test_Workflow 2", "objectType": "django.contrib.auth.User", "initialPrefetch": ""}}))
        workflow = Workflow.objects.get(name="Test_Workflow 2")
        self.assertMatchSnapshot(client.execute(MUTATE_WORKFLOW_GRAPH_GQL,
            variables={
                "param": {"id": workflow.id, "name": "Test_Workflow 3", "objectType": "django.contrib.auth.User", "initialPrefetch": ""}}))

        self.assertMatchSnapshot(client.execute(LIST_WORKFLOW_GRAPH_GQL,
            variables={"param": "Test_Workflow 3"}))

        self.assertMatchSnapshot(client.execute(MUTATE_STATE_GRAPH_GQL,
            variables={
                "param": {"workflow": workflow.id, "name": "New", "initial": True, "active": True}}))
        self.assertMatchSnapshot(client.execute(LIST_STATES_GQL))

    def test_clone(self):
        wf = workflow.get_workflow("Test_Workflow")
        old_id = wf.id
        new_name = "New Clone Test"
        new_prefetch = "{'foo':'bar'}"
        new_workflow: Workflow
        old_workflow: Workflow
        new_workflow, old_workflow, state_map, transition_map = wf.clone(name=new_name, initial_prefetch=new_prefetch)
        self.assertEqual(old_id, old_workflow.id)
        self.assertEqual(new_workflow.name, new_name)
        self.assertEqual(new_workflow.initial_prefetch, new_prefetch)
        self.assertTrue(len(set(state_map.keys()).intersection(state_map.values())) == 0, "new and old states still share values in state map")
        self.assertTrue(len(set(transition_map.keys()).intersection(transition_map.values())) == 0,
            "new and old transitions still share values in transition map")
        old_states = old_workflow.state_set.all().values_list('id', flat=True)
        new_target_states = State.objects.filter(Q(incoming_transitions__workflow=new_workflow) | Q(outgoing_transitions__workflow=new_workflow)).values_list('id', flat=True)
        self.assertTrue(len(set(new_target_states).intersection(old_states)) == 0, "new and old workflow still share states")
        client = Client(schema)
        self.assertMatchSnapshot(client.execute(LIST_WORKFLOWS_GQL))
        self.assertMatchSnapshot(client.execute(LIST_WORKFLOW_GRAPH_GQL))

