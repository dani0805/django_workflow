===============
Django Workflow
===============

This project aim is to provide a simple database driven workflow engine that you can use to configure and
automate complex operations. It is based on configurable state machines that are defined at runtime through the admin
interface.

----

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

