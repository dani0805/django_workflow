import threading
import json
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy

# import a definition from a module at runtime
from django_workflow.utils import import_from, import_from_path


class WorkflowManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Workflow(models.Model):
    objects = WorkflowManager()

    name = models.CharField(max_length=50, unique=True, verbose_name=ugettext_lazy("Name"))
    object_type = models.CharField(max_length=200, verbose_name=ugettext_lazy("Object_Type"))
    initial_prefetch = models.CharField(max_length=4000, null=True, blank=True, verbose_name=ugettext_lazy("Object_Type"))

    @property
    def initial_prefetch_dict(self):
        return json.loads(self.initial_prefetch) if self.initial_prefetch else None

    @property
    def initial_state(self):
        return State.objects.get(workflow=self, initial=True)

    @property
    def initial_transition(self):
        return Transition.objects.get(workflow=self, initial_state=None, final_state=self.initial_state)

    def prefetch_initial_objects(self):
        print("fetching initial candidates")
        return self.object_class().objects.filter(**self.initial_prefetch_dict) if self.initial_prefetch else None

    def __unicode__(self):
        return self.name

    def is_initial_transition_available(self, user, object_id, automatic=False):
        obj = CurrentObjectState.objects.filter(object_id=object_id)
        if not obj.exists():
            conditions = self.initial_transition.condition_set.all()
            if len(conditions) == 0:
                if automatic:
                    return self.initial_transition.automatic
                else:
                    return not self.initial_transition.automatic
            else:
                root_condition = conditions.first()
                if root_condition.check_condition(user, object_id):
                    if automatic:
                        return self.initial_transition.automatic
                    else:
                        return not self.initial_transition.automatic
                else:
                    return False
        else:
            return False

    def natural_key(self):
        return (self.name,)

    def add_object(self, object_id, async=True):
        CurrentObjectState.objects.create(object_id=object_id, state=self.initial_state)
        return _execute_atomatic_transitions(self.initial_state, object_id, async=async)

    def object_class(self):
        return import_from_path(self.object_type)


class StateManager(models.Manager):
    def get_by_natural_key(self, name, workflow):
        return self.get(name=name, workflow__name=workflow)


class State(models.Model):
    objects = StateManager()

    workflow = models.ForeignKey(Workflow, verbose_name=ugettext_lazy("Workflow"))
    name = models.CharField(max_length=200, verbose_name=ugettext_lazy("Name"))
    active = models.BooleanField(verbose_name=ugettext_lazy("Active"))
    initial = models.BooleanField(default=False, verbose_name=ugettext_lazy("Initial"))

    class Meta:
        unique_together = (('name', 'workflow'),)

    def __unicode__(self):
        return "{}: {}".format(self.workflow.name, self.name)

    def natural_key(self):
        return (self.name, self.workflow.name)

    def available_transitions(self, user, object_id, automatic=False):
        return [t for t in self.outgoing_transitions.all() if t.is_available(user, object_id, automatic)]


class TransitionManager(models.Manager):
    def get_by_natural_key(self, name, workflow, final_state):
        return self.get(
            name=name,
            final_state__workflow__name=workflow,
            final_state__name=final_state
        )


class Transition(models.Model):
    objects = TransitionManager()

    workflow = models.ForeignKey(Workflow, verbose_name=ugettext_lazy("Workflow"), editable=False)
    name = models.CharField(max_length=200, verbose_name=ugettext_lazy("Name"))
    description = models.CharField(max_length=400, null=True, blank=True, verbose_name=ugettext_lazy("Description"))
    initial_state = models.ForeignKey(State, null=True, blank=True, verbose_name=ugettext_lazy("Initial State"),
                                      related_name="outgoing_transitions")
    final_state = models.ForeignKey(State, verbose_name=ugettext_lazy("Final State"),
                                    related_name="incoming_transitions")
    priority = models.IntegerField(null=True, blank=True, verbose_name=ugettext_lazy("Priority"))
    automatic = models.BooleanField(verbose_name=ugettext_lazy("Automatic"))
    automatic_delay = models.FloatField(null=True, blank=True, verbose_name=ugettext_lazy("Automatic Delay in Days"))

    class Meta:
        ordering = ["priority"]
        unique_together = (('name', 'final_state'),)

    @property
    def is_initial(self):
        return self.initial_state is None

    def __unicode__(self):
        return "{}{}: {} to {}".format(self.final_state.workflow.name, "(" + self.name + ")" if self.name else "",
                                       self.initial_state.name if self.initial_state else "START", self.final_state.name)

    def natural_key(self):
        return (self.name, self.final_state.workflow.name, self.final_state.name)

    def save(self, **qwargs):
        if self.initial_state:
            self.workflow = self.initial_state.workflow
        else:
            self.workflow = self.final_state.workflow
        super(Transition, self).save(**qwargs)

    def is_available(self, user, object_id, automatic=False):
        if self.is_initial:
            return self.workflow.is_initial_transition_available(user, object_id, automatic=automatic)
        obj = CurrentObjectState.objects.filter(object_id=object_id, state__id=self.initial_state.id)
        if obj.exists():
            obj = obj.first()
            conditions = self.condition_set.all()
            if len(conditions) == 0:
                if automatic:
                    return self.automatic and self.automatic_delay is None or timezone.now() - obj.updated_ts > timedelta(
                        days=self.automatic_delay)
                else:
                    return not self.automatic
            else:
                root_condition = conditions.first()
                if root_condition.check_condition(user, object_id):
                    if automatic:
                        return self.automatic and self.automatic_delay is None or timezone.now() - obj.updated_ts > timedelta(
                            days=self.automatic_delay)
                    else:
                        return not self.automatic
                else:
                    return False
        else:
            return False

    def execute(self, user, object_id, async=False, automatic=False):
        if async:
            thr = threading.Thread(target=_execute_transition, args=(self, user, object_id),
                                   kwargs={"automatic": automatic})
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
            thr = threading.Thread(target=c.function, args=(transition.initial_state.workflow, user, object_id),
                                   kwargs=params)
            thr.start()
        # finally look for the first automatic transaction that applies and start it if any
        _execute_atomatic_transitions(transition.final_state, object_id)


def _execute_atomatic_transitions(state, object_id, async=True):
    if not state.active:
        return
    automatic_transitions = state.outgoing_transitions.filter(automatic=True)
    for t in automatic_transitions:
        if t.is_available(None, object_id, automatic=True):
            return t.execute(None, object_id, async=async, automatic=True)


@transaction.atomic
def _atomic_execution(object_id, transition, user):
    for c in transition.callback_set.filter(execute_async=False):
        params = {p.name: p.value for p in c.parameters.all()}
        c.function(transition.initial_state.workflow, user, object_id, **params)
    if transition.initial_state is not None:
        objState = CurrentObjectState.objects.get(object_id=object_id, state__workflow=transition.initial_state.workflow)
        objState.state = transition.final_state
        objState.save()
    else:
        CurrentObjectState.objects.create(object_id=object_id, state=transition.final_state)
    TransitionLog.objects.create(object_id=object_id, user_id=user.id if user else None, transition=transition,
                                 success=True)


class Condition(models.Model):
    CONDITION_TYPES = [
        ("function", "Function Call"),
        ("and", "Boolean AND"),
        ("or", "Boolean OR"),
        ("not", "Boolean NOT"),
    ]
    workflow = models.ForeignKey(Workflow, verbose_name=ugettext_lazy("Workflow"), editable=False)
    condition_type = models.CharField(max_length=10, choices=CONDITION_TYPES, verbose_name=ugettext_lazy("Type"))
    parent_condition = models.ForeignKey("Condition", null=True, blank=True,
                                         verbose_name=ugettext_lazy("Parent Condition"),
                                         related_name="child_conditions")
    transition = models.ForeignKey(Transition, null=True, blank=True, verbose_name=ugettext_lazy("Transition"))

    def clean(self):
        if self.transition and self.parent_condition:
            raise ValidationError("cannot specifiy both transition and parent condition")
        elif not self.transition and not self.parent_condition:
            raise ValidationError("at least one of transition and parent condition must be not null")

    def save(self, **qwargs):
        if self.transition:
            self.workflow = self.transition.workflow
        else:
            self.workflow = self.parent_condition.workflow
        super(Condition, self).save(**qwargs)

    def __unicode__(self):
        ancestors = []
        transition = self.transition
        p = self.parent_condition
        while p is not None:
            transition = p.transition
            ancestors.insert(0, p.condition_type)
            p = p.parent_condition
        return "{}: {} -> {}".format(transition, ancestors, self.condition_type)

    def check_condition(self, user, object_id):
        if self.condition_type == "function":
            func = self.function_set.first()
            call = func.function
            params = {p.name: p.value for p in func.parameters.all()}
            wf = self.transition.workflow
            return call(wf, user, object_id, **params)
            # Not recursive
        elif self.condition_type == "not":
            return not self.child_conditions.first().check_condition(user, object_id)
            # Recursive
        elif self.condition_type == "and":
            return all([c.check_condition(user, object_id) for c in self.child_conditions.all()])
            # Recursive
        elif self.condition_type == "or":
            return any([c.check_condition(user, object_id) for c in self.child_conditions.all()])


class Function(models.Model):
    workflow = models.ForeignKey(Workflow, verbose_name=ugettext_lazy("Workflow"), editable=False)
    function_name = models.CharField(max_length=200, verbose_name=ugettext_lazy("Function"))
    function_module = models.CharField(max_length=400, verbose_name=ugettext_lazy("Module"))
    condition = models.ForeignKey(Condition, verbose_name=ugettext_lazy("Condition"))

    def __unicode__(self):
        return "{} - {}.{}".format(self.condition, self.function_module, self.function_name)

    def save(self, **qwargs):
        self.workflow = self.condition.workflow
        super(Function, self).save(**qwargs)

    @property
    def function(self):
        return import_from(self.function_module, self.function_name)


class FunctionParameter(models.Model):
    workflow = models.ForeignKey(Workflow, verbose_name=ugettext_lazy("Workflow"), editable=False)
    function = models.ForeignKey(Function, verbose_name=ugettext_lazy("Function"), related_name="parameters")
    name = models.CharField(max_length=100, verbose_name=ugettext_lazy("Name"))
    value = models.CharField(max_length=4000, verbose_name=ugettext_lazy("Value"))

    def __unicode__(self):
        return "{} ({}: {})".format(self.function, self.name, self.value)

    def save(self, **qwargs):
        self.workflow = self.function.workflow
        super(FunctionParameter, self).save(**qwargs)


class Callback(models.Model):
    workflow = models.ForeignKey(Workflow, verbose_name=ugettext_lazy("Workflow"), editable=False)
    function_name = models.CharField(max_length=200, verbose_name=ugettext_lazy("Name"))
    function_module = models.CharField(max_length=400, verbose_name=ugettext_lazy("Module"))
    transition = models.ForeignKey(Transition, verbose_name=ugettext_lazy("Transition"))
    order = models.IntegerField(verbose_name=ugettext_lazy("Order"))
    execute_async = models.BooleanField(verbose_name=ugettext_lazy("Execute Asynchronously"), default=False)

    def save(self, **qwargs):
        self.workflow = self.transition.workflow
        super(Callback, self).save(**qwargs)

    @property
    def function(self):
        return import_from(self.function_module, self.function_name)

    class Meta:
        ordering = ["order"]


class CallbackParameter(models.Model):
    workflow = models.ForeignKey(Workflow, verbose_name=ugettext_lazy("Workflow"), editable=False)
    callback = models.ForeignKey(Callback, verbose_name=ugettext_lazy("Callback"), related_name="parameters")
    name = models.CharField(max_length=100, verbose_name=ugettext_lazy("Name"))
    value = models.CharField(max_length=4000, verbose_name=ugettext_lazy("Value"))

    def save(self, **qwargs):
        self.workflow = self.callback.workflow
        super(CallbackParameter, self).save(**qwargs)


class CurrentObjectState(models.Model):
    workflow = models.ForeignKey(Workflow, verbose_name=ugettext_lazy("Workflow"), editable=False)
    object_id = models.CharField(max_length=200, verbose_name=ugettext_lazy("Object Id"))
    state = models.ForeignKey(State, verbose_name=ugettext_lazy("State"))
    updated_ts = models.DateTimeField(auto_now=True, verbose_name=ugettext_lazy("Last Updated"))

    def __unicode__(self):
        return "{} in state {} since {}".format(self.object_id, self.state, self.updated_ts)

    def save(self, **qwargs):
        self.workflow = self.state.workflow
        super(CurrentObjectState, self).save(**qwargs)


class TransitionLog(models.Model):
    workflow = models.ForeignKey(Workflow, verbose_name=ugettext_lazy("Workflow"), editable=False)
    user_id = models.IntegerField(blank=True, null=True, verbose_name=ugettext_lazy("User Id"))
    object_id = models.IntegerField(verbose_name=ugettext_lazy("Object Id"))
    transition = models.ForeignKey(Transition, verbose_name=ugettext_lazy("Transition"))
    completed_ts = models.DateTimeField(auto_now=True, verbose_name=ugettext_lazy("Time of Completion"))
    success = models.BooleanField(verbose_name=ugettext_lazy("Success"))
    ERROR_CODES = [
        ("400", "400 - Not Authorized"),
        ("500", "500 - Internal Error"),
    ]
    error_code = models.CharField(max_length=5, null=True, blank=True, choices=ERROR_CODES,
                                  verbose_name=ugettext_lazy("Error Code"))
    error_message = models.CharField(max_length=4000, null=True, blank=True,
                                     verbose_name=ugettext_lazy("Error Message"))

    def save(self, **qwargs):
        self.workflow = self.transition.workflow
        super(TransitionLog, self).save(**qwargs)
