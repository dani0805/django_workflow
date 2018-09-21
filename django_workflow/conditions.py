# import a definition from a module at runtime
import ast
import numbers

from django.db.models.manager import Manager

from django_workflow.utils import import_from, import_from_path

def object_attribute_value(*, workflow, object_id, user, object_state, **kwargs):
    params = parse_parameters(workflow=workflow, object_id=object_id, user=user, object_state=object_state, **kwargs)
    if "attribute_name" in params:
        attribute_name = params.pop('attribute_name')
        object = workflow.object_class().objects.get(id=object_id)
        attribute = getattr(object, attribute_name)
        if "attribute_value" in params:
            attribute_value = params.pop('attribute_value')
            #print("comparing {} with {}".format(attribute, attribute_value))
            return attribute == attribute_value
    raise ValueError("missing parameter attribute_name or attribute_value")


def user_attribute_value(*, workflow, object_id, user, object_state, **kwargs):
    params = parse_parameters(workflow=workflow, object_id=object_id, user=user, object_state=object_state, **kwargs)
    if "attribute_name" in params:
        attribute_name = params.pop('attribute_name')
        attribute = getattr(user, attribute_name)
        if "attribute_value" in params:
            attribute_value = params.pop('attribute_value')
            return attribute == attribute_value
    raise ValueError("missing parameter attribute_name or attribute_value")

def object_attribute_filter_exist(*, workflow, object_id, user, object_state, **kwargs):
    params = parse_parameters(workflow=workflow, object_id=object_id, user=user, object_state=object_state, **kwargs)
    if "attribute_name" in params:
        attribute_name = params.pop('attribute_name')
        object = workflow.object_class().objects.get(id=object_id)
        attribute = getattr(object, attribute_name)
        return attribute.filter(**params).exists()
    else:
        raise ValueError("missing parameter attribute_name")


def user_attribute_filter_exist(*, workflow, object_id, user, object_state, **kwargs):
    params = parse_parameters(workflow=workflow, object_id=object_id, user=user, object_state=object_state, **kwargs)
    if "attribute_name" in params:
        attribute_name = params.pop('attribute_name')
        attribute = getattr(user, attribute_name)
        return attribute.filter(**params).exists()
    else:
        raise ValueError("missing parameter attribute_name")


def object_filter_exist(*, workflow, object_id, user, object_state, **kwargs):
    params = parse_parameters(workflow=workflow, object_id=object_id, user=user, object_state=object_state, **kwargs)
    return workflow.object_class().objects.filter(**params).exists()


def user_filter_exist(*, workflow, object_id, user, object_state, **kwargs):
    params = parse_parameters(workflow=workflow, object_id=object_id, user=user, object_state=object_state, **kwargs)
    return type(user).objects.filter(**params).exists()


def other_filter_exist(*, workflow, object_id, user, object_state, **kwargs):
    params = parse_parameters(workflow=workflow, object_id=object_id, user=user, object_state=object_state, **kwargs)
    if "model_type" in params:
        model_type = import_from_path(params.pop('model_type'))
        return model_type.objects.filter(**params).exists()
    else:
        raise ValueError("missing parameter model_type")


def parse_parameters(*, workflow, object_id, user, object_state, **kwargs):
    params = dict()
    #print(filter)
    for k, v in kwargs.items():
        params.update({k: parse_value(v, object_id, user, workflow)})
    return params


def parse_value(value, object_id, user, workflow):
    #print(value)
    if value.strip().startswith("{{") and value.endswith("}}"):
        parts = value[2:-2].split(".")
        o = None
        if parts[0].strip() == "user":
            o = user
        elif parts[0].strip() == "object":
            o = workflow.object_class().objects.get(id=object_id)
        else:
            raise ValueError("dynamic parameter values must start with user or object")
        if len(parts) > 1:
            for p in parts[1:]:
                #print("intermediate object value {}: {}".format(type(o), o))
                o = getattr(o, p.strip(), None)
                if o == None:
                    continue
        #print("intermediate object value {}: {}".format(type(o), o))
        return o
    else:
        # try to parse a literal
        try:
            return ast.literal_eval(value)
        except ValueError:
            # assume is a string
            return value
