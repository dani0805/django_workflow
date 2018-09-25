import threading
import json
from datetime import timedelta, datetime

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import SET_NULL
from django.utils.timezone import now as django_now
from django.utils.translation import ugettext_lazy
from django.db.models.deletion import PROTECT

# import a definition from a module at runtime
from django_workflow.utils import import_from, import_from_path


class WorkflowManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Workflow(models.Model):
    objects = WorkflowManager()

    name = models.CharField(max_length=200, unique=True, verbose_name=ugettext_lazy("Name"))
    object_type = models.CharField(max_length=200, verbose_name=ugettext_lazy("Object_Type"))
    initial_prefetch = models.CharField(max_length=4000, null=True, blank=True, verbose_name=ugettext_lazy("Object_Type"))

    @property
    def initial_prefetch_dict(self):
        dict = json.loads(self.initial_prefetch) if self.initial_prefetch else None
        for k,v in dict.items():
            if "today" in v:
                sum_operands = [x.strip() for x in v.split("+")]
                res = None
                for sum_op in sum_operands:
                    sub_operands = [x.strip() for x in sum_op.split("-")]
                    sub_res = None
                    for sub_op in sub_operands:
                        mul_operands = [x.strip() for x in sub_op.split("*")]
                        mul_res = None
                        for mul_op in mul_operands:
                            div_res = None
                            div_operands = [x.strip() for x in mul_op.split("/")]
                            for op in div_operands:
                                if div_res is None:
                                    div_res = datetime.now().date() if op == "today" else float(op)
                                else:
                                    div_res = div_res / float(op) #you cannot divide by today
                            if mul_res is None:
                                mul_res = div_res
                            else:
                                mul_res = mul_res * div_res
                        # perform multiplications and divisions in float, then convert to timedelta for the rest
                        if isinstance(mul_res, float):
                            mul_res = timedelta(seconds=mul_res)
                        if sub_res is None:
                            sub_res = mul_res
                        else:
                            sub_res = sub_res - mul_res
                    if res is None:
                        res = sub_res
                    else:
                        res = res + sub_res
                res = res.strftime("%Y-%m-%dT%H:%M:%SZ")
                dict.update({k:res})
        return dict



    @property
    def initial_state(self):
        return State.objects.get(workflow=self, initial=True)

    @property
    def initial_transition(self):
        return Transition.objects.filter(workflow=self, initial_state=None, final_state=self.initial_state).first()

    def prefetch_initial_objects(self):
        objects = self\
            .object_class().objects.filter(**self.initial_prefetch_dict)\
            .exclude(id__in=CurrentObjectState.objects.filter(workflow=self).values_list("object_id", flat=True)) if self.initial_prefetch else []
        return objects

    def __unicode__(self):
        return self.name

    def is_initial_transition_available(self, *, user, object_id, object_state_id=None, automatic=False):
        if object_state_id:
            return not CurrentObjectState.objects.filter(id=object_state_id, workflow=self).exists()
        else:
            last = CurrentObjectState.objects.filter(object_id=object_id, workflow=self).order_by('-id').first()
            if last and last.state.active:
                return False
            elif self.initial_transition is not None:
                conditions = self.initial_transition.condition_set.all()
                if len(conditions) == 0:
                    if automatic:
                        return self.initial_transition.automatic
                    else:
                        return not self.initial_transition.automatic
                else:
                    root_condition = conditions.first()
                    if root_condition.check_condition(user=user, object_id=object_id, object_state=last):
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
        process = CurrentObjectState.objects.create(object_id=object_id, state=self.initial_state)
        _execute_atomatic_transitions(self.initial_state, object_id, process, async=async)
        return process

    def object_class(self):
        return import_from_path(self.object_type)

    def transition_by_name(self, name):
        transition = Transition.objects.filter(workflow=self, name__iexact=name)
        if len(transition) > 0:
            return transition.first()
        return None


class StateManager(models.Manager):
    def get_by_natural_key(self, name, workflow):
        return self.get(name=name, workflow__name=workflow)


class State(models.Model):
    objects = StateManager()

    workflow = models.ForeignKey(Workflow, on_delete=PROTECT, verbose_name=ugettext_lazy("Workflow"))
    name = models.CharField(max_length=200, verbose_name=ugettext_lazy("Name"))
    active = models.BooleanField(verbose_name=ugettext_lazy("Active"))
    initial = models.BooleanField(default=False, verbose_name=ugettext_lazy("Initial"))

    class Meta:
        unique_together = (('name', 'workflow'),)

    def __unicode__(self):
        return "{}: {}".format(self.workflow.name, self.name)

    @property
    def is_final_state(self):
        return self.outgoing_transitions.count() == 0

    def natural_key(self):
        return (self.name, self.workflow.name)

    def available_transitions(self, user, object_id, automatic=False):
        return [t for t in self.outgoing_transitions.all() if t.is_available(user=user, object_id=object_id, automatic=automatic)]


class StateVariableDefManager(models.Manager):

    def get_by_natural_key(self, name, workflow):
        return self.get(name=name, workflow__name=workflow)


class StateVariableDef(models.Model):
    objects = StateVariableDefManager()
    workflow = models.ForeignKey(Workflow, on_delete=PROTECT, verbose_name=ugettext_lazy("Workflow"))
    state = models.ForeignKey(State, on_delete=PROTECT, verbose_name=ugettext_lazy("State"),
        related_name="variable_definitions")
    name = models.CharField(max_length=100, verbose_name=ugettext_lazy("Name"))

    class Meta:
        unique_together = (('name', 'workflow', 'state'),)

    def __unicode__(self):
        return "{}: {} - {}".format(self.workflow.name, self.state.name, self.name)

    def natural_key(self):
        return self.name, self.state.name, self.workflow.name


class TransitionManager(models.Manager):

    def get_by_natural_key(self, name, workflow, initial_state, final_state):
        return self.get(
            name=name,
            workflow__name=workflow,
            initial_state__name=initial_state,
            final_state__name=final_state
        )


class Transition(models.Model):
    objects = TransitionManager()

    workflow = models.ForeignKey(Workflow, on_delete=PROTECT, verbose_name=ugettext_lazy("Workflow"), editable=False)
    name = models.CharField(max_length=50, verbose_name=ugettext_lazy("Name"))
    description = models.CharField(max_length=400, null=True, blank=True, verbose_name=ugettext_lazy("Description"))
    initial_state = models.ForeignKey(State, on_delete=SET_NULL, null=True, blank=True, verbose_name=ugettext_lazy("Initial State"),
                                      related_name="outgoing_transitions")
    final_state = models.ForeignKey(State, on_delete=PROTECT, verbose_name=ugettext_lazy("Final State"),
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
        return (self.name, self.workflow.name, self.initial_state.name if self.initial_state else None, self.final_state.name)

    def save(self, **qwargs):
        if self.initial_state:
            self.workflow = self.initial_state.workflow
        else:
            self.workflow = self.final_state.workflow
        super(Transition, self).save(**qwargs)

    def is_available(self, *, user, object_id, object_state_id=None, automatic=False, last_transition=None):
        return _is_transition_available(self, user, object_id, object_state_id=object_state_id, automatic=automatic, last_transition=last_transition)

    def execute(self, user, object_id, object_state_id=None, async=False, automatic=False):
        if async:
            thr = threading.Thread(target=_execute_transition, args=(self, user, object_id, object_state_id),
                                   kwargs={"automatic": automatic})
            thr.start()
            return thr
        else:
            return _execute_transition(transition=self, user=user, object_id=object_id, object_state_id=object_state_id, automatic=automatic)


class Condition(models.Model):
    CONDITION_TYPES = [
        ("function", "Function Call"),
        ("and", "Boolean AND"),
        ("or", "Boolean OR"),
        ("not", "Boolean NOT"),
    ]
    workflow = models.ForeignKey(Workflow, on_delete=PROTECT, verbose_name=ugettext_lazy("Workflow"), editable=False)
    condition_type = models.CharField(max_length=10, choices=CONDITION_TYPES, verbose_name=ugettext_lazy("Type"))
    parent_condition = models.ForeignKey("Condition", on_delete=SET_NULL, null=True, blank=True,
                                         verbose_name=ugettext_lazy("Parent Condition"),
                                         related_name="child_conditions")
    transition = models.ForeignKey(Transition, on_delete=SET_NULL, null=True, blank=True, verbose_name=ugettext_lazy("Transition"))

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

    def check_condition(self, *, object_id, user, object_state):
        if self.condition_type == "function":
            func = self.function_set.first()
            call = func.function
            params = {p.name: p.value for p in func.parameters.all()}
            wf = self.workflow
            result = call(workflow=wf, user=user, object_id=object_id, object_state=object_state, **params)
            if result is None:
                result = False
            #print("{}.{} ({}, {}, {}, **{}) = {}".format(func.function_module,func.function_name, wf, user, object_id, params, result))
            return result
            # Not recursive
        elif self.condition_type == "not":
            return not self.child_conditions.first().check_condition(user=user, object_id=object_id, object_state=object_state)
            # Recursive
        elif self.condition_type == "and":
            return all([c.check_condition(user=user, object_id=object_id, object_state=object_state) for c in self.child_conditions.all()])
            # Recursive
        elif self.condition_type == "or":
            return any([c.check_condition(user=user, object_id=object_id, object_state=object_state) for c in self.child_conditions.all()])


class Function(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=PROTECT, verbose_name=ugettext_lazy("Workflow"), editable=False)
    function_name = models.CharField(max_length=200, verbose_name=ugettext_lazy("Function"))
    function_module = models.CharField(max_length=400, verbose_name=ugettext_lazy("Module"))
    condition = models.ForeignKey(Condition, on_delete=PROTECT, verbose_name=ugettext_lazy("Condition"))

    def __unicode__(self):
        return "{} - {}.{}".format(self.condition, self.function_module, self.function_name)

    def save(self, **qwargs):
        self.workflow = self.condition.workflow
        super(Function, self).save(**qwargs)

    @property
    def function(self):
        return import_from(self.function_module, self.function_name)


class FunctionParameter(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=PROTECT, verbose_name=ugettext_lazy("Workflow"), editable=False)
    function = models.ForeignKey(Function, on_delete=PROTECT, verbose_name=ugettext_lazy("Function"), related_name="parameters")
    name = models.CharField(max_length=100, verbose_name=ugettext_lazy("Name"))
    value = models.CharField(max_length=4000, verbose_name=ugettext_lazy("Value"))

    def __unicode__(self):
        return "{} ({}: {})".format(self.function, self.name, self.value)

    def save(self, **qwargs):
        self.workflow = self.function.workflow
        super(FunctionParameter, self).save(**qwargs)


class Callback(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=PROTECT, verbose_name=ugettext_lazy("Workflow"), editable=False)
    function_name = models.CharField(max_length=200, verbose_name=ugettext_lazy("Name"))
    function_module = models.CharField(max_length=400, verbose_name=ugettext_lazy("Module"))
    transition = models.ForeignKey(Transition, on_delete=PROTECT, verbose_name=ugettext_lazy("Transition"))
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
    workflow = models.ForeignKey(Workflow, on_delete=PROTECT, verbose_name=ugettext_lazy("Workflow"), editable=False)
    callback = models.ForeignKey(Callback, on_delete=PROTECT, verbose_name=ugettext_lazy("Callback"), related_name="parameters")
    name = models.CharField(max_length=100, verbose_name=ugettext_lazy("Name"))
    value = models.CharField(max_length=4000, verbose_name=ugettext_lazy("Value"))

    def save(self, **qwargs):
        self.workflow = self.callback.workflow
        super(CallbackParameter, self).save(**qwargs)


class CurrentObjectState(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=PROTECT, verbose_name=ugettext_lazy("Workflow"), editable=False)
    object_id = models.CharField(max_length=200, verbose_name=ugettext_lazy("Object Id"))
    state = models.ForeignKey(State, on_delete=PROTECT, verbose_name=ugettext_lazy("State"))
    updated_ts = models.DateTimeField(auto_now=True, verbose_name=ugettext_lazy("Last Updated"))

    class Meta:
        indexes = [
            models.Index(fields=['workflow', 'object_id']),
        ]

    def __unicode__(self):
        return "{} in state {} since {}".format(self.object_id, self.state, self.updated_ts)

    def save(self, **qwargs):
        self.workflow = self.state.workflow
        super(CurrentObjectState, self).save(**qwargs)


class TransitionLog(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=PROTECT, verbose_name=ugettext_lazy("Workflow"), editable=False)
    user_id = models.IntegerField(blank=True, null=True, verbose_name=ugettext_lazy("User Id"))
    object_id = models.IntegerField(verbose_name=ugettext_lazy("Object Id"))
    transition = models.ForeignKey(Transition, on_delete=PROTECT, verbose_name=ugettext_lazy("Transition"))
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


def _is_transition_available(transition, user, object_id, object_state_id=None, automatic=False, last_transition=None):
    #print("checking if {} available on obj id {}".format(transition.name, object_id))
    if transition.is_initial:
        return transition.workflow.is_initial_transition_available(user=user, object_id=object_id, object_state_id=object_state_id,
            automatic=automatic)
    object_state = None
    if object_state_id is not None:
        object_state = CurrentObjectState.objects.get(id=object_state_id)
    else:
        q = CurrentObjectState.objects.filter(object_id=object_id, workflow=transition.workflow)
        if q.exists():
            object_state = q.first()
    if object_state is not None:
        if last_transition is None:
            last_transition = object_state.updated_ts
        if automatic != transition.automatic:
            #print("not executing because of automatic setting")
            return False
        if automatic \
                and transition.automatic_delay is not None \
                and last_transition is not None \
                and django_now() - last_transition < timedelta(days=transition.automatic_delay):
            #print("not executing because of delay")
            return False
        root_condition = transition.condition_set.filter(parent_condition__isnull=True)
        condition_checks = True
        if root_condition.exists():
            condition_checks = root_condition.first().check_condition(user=user, object_id=object_id, object_state=object_state)
        #print("condition_checks: {}".format(condition_checks))
        return condition_checks
    else:
        return False


def _execute_transition(*, transition, user, object_id, object_state_id, automatic=False, last_transition=None,
        recursion_count=0):
    if recursion_count > 10:
        raise RecursionError("too many chained automatic transitions")
    if transition.is_available(user=user, object_id=object_id, object_state_id=object_state_id, automatic=automatic, last_transition=last_transition):
        # print("transition {} available on {}".format(transition, object_id))
        # first execute all sync callbacks within then update the log and state tables all within a transaction
        object_state = _atomic_execution(object_id, object_state_id, transition, user)
        # now trigger all async callbacks
        for c in transition.callback_set.filter(execute_async=True):
            params = {p.name: p.value for p in c.callback_parameter_set.all()}
            thr = threading.Thread(target=c.function, args=(transition.initial_state.workflow, user, object_id),
                kwargs=params)
            thr.start()
        # finally look for the first automatic transaction that applies and start it if any
        _execute_atomatic_transitions(transition.final_state, object_id, object_state_id,
            last_transition=django_now())
        return object_state


def _execute_atomatic_transitions(state, object_id, object_state_id, async=False, last_transition=None):
    if not state.active:
        return None
    automatic_transitions = state.outgoing_transitions.filter(automatic=True)
    for t in automatic_transitions:
        if t.is_available(user=None, object_id=object_id, object_state_id=object_state_id, automatic=True):
            return _execute_transition(transition=t, user=None, object_id=object_id, object_state_id=object_state_id, automatic=True, last_transition=last_transition)


@transaction.atomic
def _atomic_execution(object_id, object_state_id, transition, user):
    # we first change status for consistency, exceptions in callbacks could break the process
    # print("executing transition {} on object id {}".format(transition.name, object_id))
    object_state = None
    if transition.initial_state is not None:
        if object_state_id:
            object_state = CurrentObjectState.objects.get(id=object_state_id, state__workflow=transition.workflow)
        else:
            object_state = CurrentObjectState.objects.filter(object_id=object_id,
                state__workflow=transition.workflow).order_by('-id').first()
        if object_state:
            object_state.updated_ts = django_now()
            object_state.state = transition.final_state
            object_state.save()
    else:
        object_state = CurrentObjectState.objects.create(object_id=object_id, state=transition.final_state)
    for c in transition.callback_set.filter(execute_async=False):
        # print("executing {}.{}".format(c.function_module, c.function_name))
        params = {p.name: p.value for p in c.parameters.all()}
        c.function(workflow=transition.final_state.workflow, user=user, object_id=object_id, object_state=object_state, **params)
    TransitionLog.objects.create(object_id=object_id, user_id=user.id if user else None, transition=transition,
        success=True)
    return object_state


class StateVariable(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=PROTECT, verbose_name=ugettext_lazy("Workflow"), editable=False)
    current_object_state = models.ForeignKey(CurrentObjectState, on_delete=PROTECT, verbose_name=ugettext_lazy("Object State"))
    state_variable_def = models.ForeignKey(StateVariableDef, on_delete=PROTECT,
        verbose_name=ugettext_lazy("Variable Definition"))
    value = models.CharField(max_length=4000, verbose_name=ugettext_lazy("Value"))


