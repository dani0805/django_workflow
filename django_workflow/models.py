import threading

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.translation import ugettext_lazy

# import a definition from a module at runtime
from django_workflow.utils import import_from, import_from_path


class Workflow(models.Model):
    name = models.CharField(max_length=200, verbose_name=ugettext_lazy("Name"))
    object_type = models.CharField(max_length=200, verbose_name=ugettext_lazy("Object_Type"))
    initial_state = models.OneToOneField("State", null=True, blank=True, verbose_name=ugettext_lazy("Initial State"), related_name="starts_workflow")

    def __unicode__(self):
        return self.name

    def add_object(self, object_id, async=True):
        CurrentObjectState.objects.create(object_id=object_id, state=self.initial_state)
        return _execute_atomatic_transitions(self.initial_state, object_id, async=async)

    def object_class(self):
        return import_from_path(self.object_type)



class State(models.Model):
    name = models.CharField(max_length=200, verbose_name=ugettext_lazy("Name"))
    workflow = models.ForeignKey(Workflow, verbose_name=ugettext_lazy("Workflow"))
    active = models.BooleanField( verbose_name=ugettext_lazy("Active"))

    def __unicode__(self):
        return "{}: {}".format(self.workflow.name, self.name)

    def available_transitions(self, user, object_id, automatic=False):
        return [t for t in self.outgoing_transitions.all() if t.is_available(user, object_id, automatic)]


class Transition(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name=ugettext_lazy("Name"))
    initial_state = models.ForeignKey(State, verbose_name=ugettext_lazy("Initial State"), related_name="outgoing_transitions")
    final_state = models.ForeignKey(State, verbose_name=ugettext_lazy("Final State"),
        related_name="incoming_transitions")
    priority = models.IntegerField(null=True, blank=True, verbose_name=ugettext_lazy("Priority"))
    automatic = models.BooleanField(verbose_name=ugettext_lazy("Automatic"))
    automatic_delay = models.FloatField(null=True, blank=True, verbose_name=ugettext_lazy("Automatic Delay in Days"))

    class Meta:
        ordering = ["priority"]

    def __unicode__(self):
        return "{}{}: {} to {}".format(self.initial_state.workflow.name, "("+self.name+")" if self.name else "", self.initial_state.name, self.final_state.name)

    def is_available(self, user, object_id, automatic=False):
        #print("checking {}". format(self))
        #print("object_id: {}, state: {}".format(object_id, self.initial_state.id))
        #print(CurrentObjectState.objects.all())
        if CurrentObjectState.objects.filter(object_id=object_id, state__id=self.initial_state.id).exists():
            conditions = self.condition_set.all()
            if len(conditions) == 0:
                #print("... no conditions")
                return self.automatic == automatic
            else:
                root_condition = conditions.first()
                #print("... root condition: {}".format(root_condition))
                return root_condition.check_condition(object_id, user ) and self.automatic == automatic
        else:
            return False

    def execute(self, user, object_id, async=False, automatic=False):
        if async:
            thr = threading.Thread(target=_execute_transition, args=(self, user, object_id), kwargs={"automatic":automatic})
            thr.start()
            return thr
        else:
            _execute_transition(self, user, object_id, automatic=automatic)


def _execute_transition(transition, user, object_id, automatic=False):
    if transition.is_available(user, object_id, automatic=automatic):
        # first execute all sync callbacks within then update the log and state tables all within a transaction
        _atomic_execution(object_id, transition, user)
        # now trigger all async callbacks
        for c in transition.callback_set.filter(execute_async=True):
            params = {p.name: p.value for p in c.callback_parameter_set.all()}
            thr = threading.Thread(target=c.function, args=(transition.initial_state.workflow, user, object_id), kwargs=params)
            thr.start()
        # finally look for the first automatic transaction that applies and start it if any
        _execute_atomatic_transitions(transition.final_state, object_id)


def _execute_atomatic_transitions(state, object_id, async=True):
    automatic_transitions = state.outgoing_transitions.filter(automatic=True)
    for t in automatic_transitions:
        if t.is_available(None, object_id, automatic=True):
            return t.execute(None, object_id, async=async, automatic=True)


@transaction.atomic
def _atomic_execution(object_id, transition, user):
    for c in transition.callback_set.filter(execute_async=False):
        params = {p.name: p.value for p in c.callback_parameter_set.all()}
        c.function(transition.initial_state.workflow, user, object_id, **params)
    objState = CurrentObjectState.objects.get(object_id=object_id, state__workflow=transition.initial_state.workflow)
    objState.state = transition.final_state
    objState.save()
    TransitionLog.objects.create(object_id=object_id, user_id=user.id if user else None, transition=transition, success=True)


class Condition(models.Model):
    CONDITION_TYPES = [
        ("function", "Function Call"),
        ("and", "Boolean AND"),
        ("or", "Boolean OR"),
        ("not", "Boolean NOT"),
    ]
    condition_type = models.CharField(max_length=10, choices=CONDITION_TYPES, verbose_name=ugettext_lazy("Type"))
    parent_condition = models.ForeignKey("Condition", null=True, blank=True, verbose_name=ugettext_lazy("Parent Condition"), related_name="child_conditions" )
    transition = models.ForeignKey(Transition, null=True, blank=True, verbose_name=ugettext_lazy("Transition") )

    def clean(self):
        if self.transition and self.parent_condition:
            raise ValidationError("cannot specifiy both transition and parent condition")
        elif not self.transition and not self.parent_condition:
            raise ValidationError("at least one of transition and parent condition must be not null")

    def __unicode__(self):
        ancestors = []
        transition = self.transition
        p = self.parent_condition
        while p is not None:
            transition = p.transition
            ancestors.insert(0, p.condition_type)
            p = p.parent_condition
        return "{}: {} -> {}".format(transition, ancestors, self.condition_type)

    def check_condition(self, object_id, user):
        if self.condition_type == "function":
            func = self.function_set.first()
            call = func.function
            params = {p.name: p.value for p in func.parameters.all()}
            wf = self.transition.initial_state.workflow
            return call(wf, object_id, user, **params)
            # Not recursive
        elif self.condition_type == "not":
            return not self.child_conditions.first().check_condition(object_id, user)
            # Recursive
        elif self.condition_type == "and":
            return all([c.check_condition(object_id, user) for c in self.child_conditions.all()])
            # Recursive
        elif self.condition_type == "or":
            return any([c.check_condition(object_id, user) for c in self.child_conditions.all()])


class Function(models.Model):
    function_name = models.CharField(max_length=200, verbose_name=ugettext_lazy("Function"))
    function_module = models.CharField(max_length=400, verbose_name=ugettext_lazy("Module"))
    condition = models.ForeignKey(Condition, verbose_name=ugettext_lazy("Condition"))

    def __unicode__(self):
        return "{} - {}.{}".format(self.condition, self.function_module, self.function_name)

    @property
    def function(self):
        return import_from(self.function_module, self.function_name)


class FunctionParameter(models.Model):
    function = models.ForeignKey(Function, verbose_name=ugettext_lazy("Function"), related_name="parameters")
    name = models.CharField(max_length=100, verbose_name=ugettext_lazy("Name"))
    value = models.CharField(max_length=4000, verbose_name=ugettext_lazy("Value"))

    def __unicode__(self):
        return "{} ({}: {})".format(self.function, self.name, self.value)



class Callback(models.Model):
    function_name = models.CharField(max_length=200, verbose_name=ugettext_lazy("Name"))
    function_module = models.CharField(max_length=400, verbose_name=ugettext_lazy("Module"))
    transition = models.ForeignKey(Transition, verbose_name=ugettext_lazy("Transition"))
    order = models.IntegerField(verbose_name=ugettext_lazy("Order"))
    execute_async = models.BooleanField(verbose_name=ugettext_lazy("Execute Asynchronously"), default=False)

    @property
    def function(self):
        return import_from(self.function_module, self.function_name)

    class Meta:
        ordering = ["order"]


class CallbackParameter(models.Model):
    callback = models.ForeignKey(Callback, verbose_name=ugettext_lazy("Callback"))
    name = models.CharField(max_length=100, verbose_name=ugettext_lazy("Name"))
    value = models.CharField(max_length=4000, verbose_name=ugettext_lazy("Value"))


class CurrentObjectState(models.Model):
    object_id = models.CharField(max_length=200, verbose_name=ugettext_lazy("Object Id"))
    state = models.ForeignKey(State, verbose_name=ugettext_lazy("State"))
    updated_ts = models.DateTimeField(auto_now=True, verbose_name=ugettext_lazy("Last Updated"))

    def __unicode__(self):
        return "{} in state {} since {}".format(self.object_id, self.state, self.updated_ts)


class TransitionLog(models.Model):
    user_id = models.IntegerField(blank=True, null=True, verbose_name=ugettext_lazy("User Id"))
    object_id = models.IntegerField(verbose_name=ugettext_lazy("Object Id"))
    transition = models.ForeignKey(Transition, verbose_name=ugettext_lazy("Transition"))
    completed_ts = models.DateTimeField(auto_now=True, verbose_name=ugettext_lazy("Time of Completion"))
    success = models.BooleanField(verbose_name=ugettext_lazy("Success"))
    ERROR_CODES = [
        ("400", "400 - Not Authorized"),
        ("500", "500 - Internal Error"),
    ]
    error_code = models.CharField(max_length=5, null=True, blank=True, choices=ERROR_CODES, verbose_name=ugettext_lazy("Error Code"))
    error_message = models.CharField(max_length=4000, null=True, blank=True, verbose_name=ugettext_lazy("Error Message"))

