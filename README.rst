===============
Django Workflow
===============

This project aim is to provide a simple database driven workflow engine that you can use to configure and
automate complex operations. It is based on configurable state machines that are defined at runtime through the admin
interface.

Workflow Definition
-------------------

A workflow is defined by the following objects:

:Workflow: main object, it must have a unique ``name``
:State: objects which represent the nodes of the graph they are ``workflow`` specific
:Transition: Transitions can be manual or automatic,
    automatic transitions are executed asynchrnously as soon as an object reaches their intial state.
    Of course only one automatic transition can be executed at the time and it will normally change the state
    so that other transitions which were defined for the intial state cannot be executed anymore.
    Which transition is executed depends on the ``priority`` and on the related conditions
:Condition: objects which limit the execution of transitions based on the properties of the object
    which is undergoing the process, of the user or on generic queries. Conditions are hierarchical and
    can be combined using special boolean conditions
:Function: For every condition ``C`` of type function there must be a function which has value ``C`` for the condition.
    The function specifies the python function which will be called to check if the condition is fulfilled.
:FunctionParameter: Each function parameter is passed as kwarg to its ``function``
:Callback: A callback defines a python function which should be called when a transition occurs,
    usually for required side effect. The callback will be called either within the same transaction and before
    the update of the object state, if ``execute_async`` is ``False`` or after the after the status
    has been updated in an independent thread
:CallbackParameter: Each callback parameter is passed as kwarg to its ``callback``

Below you can find a simple example of a 3 states workflow with a mix of manual and automatic transitions

::

    from django.contrib.auth.models import User
    from django_workflow import workflow
    from django_workflow.models import Workflow, State, Transition, Condition, Function, FunctionParameter, Callback, CallbackParameter

    # create the main workflow object
    wf = Workflow.objects.create(name="Test_Workflow", object_type="django.contrib.auth.models.User")
    # create 3 states
    s1 = State.objects.create(name="state 1", workflow=wf, active=True, initial=True)
    s2 = State.objects.create(name="state 2", workflow=wf, active=True)
    #the final state is defined as inactive so that its skipped when scanning for automatic transitions
    s3 = State.objects.create(name="state 3", workflow=wf, active=False)
    # create the transitions, we have 2 automatic transitions from state 1 to state 2,
    # the first is going to be executed despite t4 having a better priority because
    # t1 has a lower automatic_delay
    t1 = Transition.objects.create(name="auto_fast", initial_state=s1, final_state=s2, automatic=True, automatic_delay=1.0/24.0/3600.0, priority=2)
    t4 = Transition.objects.create(name="auto_slow", initial_state=s1, final_state=s3, automatic=True,
        automatic_delay=1.0 / 24.0, priority=1)
    t2 = Transition.objects.create(initial_state=s1, final_state=s3, automatic=False)
    t3 = Transition.objects.create(initial_state=s2, final_state=s3, automatic=False)
    # we set t3 to be executed only by superusers this can be done with a object_attribute_value conditon
    c1 = Condition.objects.create(condition_typ="function", transition=t3)
    f1 = Function.objects.create(
        function_name="object_attribute_value",
        function_module="django_workflow.conditions",
        condition=c1
    )
    p11 = FunctionParameter.objects.create(function=f1, name="attribute_name", value="is_superuser")
    p12 = FunctionParameter.objects.create(function=f1, name="attribute_value", value="True")
    # we want to print out if transition 1 was executed, this can be done with a callback
    cb1 = Callback.objects.create(transition=t1, function_name="_print", function_module="django_workflow.tests", order=1)
    cp11 = CallbackParameter.objects.create(callback=cb1, name="text", value="Transition 1 Executed")


States and Transitions
----------------------
Once the workflow is defined one can add objects to the workflow

::

    obj = MyModelObject.objects.get(name="MyObjectName")
    wf = workflow.get_workflow("Test_Workflow")
    wf.add_object(obj.id)

The method ``add_object`` beside starting the tracking of the object in the state machine, it also triggers
any automatic transition available in the initial state

To check the state of an object one can use:

::

    workflow.get_object_state("Test_Workflow", object_id)

and to check for available transition, e.g. to know which buttons you can show in the UI, you can call

::

    workflow.get_available_transitions("Test_Workflow", user, object_id)

where ``user`` should be the Django user that wishes to perform the action. The ``user`` is passed to
each condition and callback so it is useful to check for authorization as well as to perform specific tasks,
e.g. notifications