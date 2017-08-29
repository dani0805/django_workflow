from django.contrib import admin

from django_workflow.models import Workflow, State, Transition, Condition, Function, FunctionParameter, Callback, \
    CallbackParameter, CurrentObjectState, TransitionLog

admin.site.register(Workflow)
admin.site.register(State)
admin.site.register(Transition)
admin.site.register(Condition)
admin.site.register(Function)
admin.site.register(FunctionParameter)
admin.site.register(Callback)
admin.site.register(CallbackParameter)
admin.site.register(CurrentObjectState)
admin.site.register(TransitionLog)
