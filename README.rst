Django Workflow
===============

This project aim is to provide a simple database driven workflow engine that you can use to configure and
automate complex operations. It is based on configurable state machines that are defined at runtime through the admin
interface.

----

A workflow is defined by the following objects:

- One `Workflow` object
- Two or more `State` objects which represent the nodes of the graph
- One or more `Transition` objects. Transitions can be manual or automatic,
  automatic transitions are executed asynchrnously as soon as an object reaches their intial state.
  Of course only one automatic transition can be executed at the time and it will normally change the state
  so that other transitions which were defined for the intial state cannot be executed anymore.
  Which transition is executed depends on the `priority` and on the related conditions
- `Condition` objects which limit the execution of transitions based on the properties of the object
  which is undergoing the process, of the user or on generic queries. Conditions are hierarchical and
  can be combined using special boolean conditions

