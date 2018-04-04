# import a definition from a module at runtime
import numbers

from django.db.models.manager import Manager

from django_workflow.utils import import_from, import_from_path

def equals(attr, val):
    if type(attr) == type(True):
        return attr == (val == "True")
    elif isinstance(attr, numbers.Number):
        return attr == float(val)
    else:
        return attr == val

def object_attribute_value(workflow, user, object_id, **filter):
    params = parse_parameters(filter, user, object_id, workflow)
    if "attribute_name" in params:
        attribute_name = params.pop('attribute_name')
        object = workflow.object_class().objects.get(id=object_id)
        attribute = getattr(object, attribute_name)
        if "attribute_value" in params:
            attribute_value = params.pop('attribute_value')
            return equals(attribute, attribute_value)
    raise ValueError("missing parameter attribute_name or attribute_value")


def user_attribute_value(workflow, user, object_id, **filter):
    params = parse_parameters(filter, user, object_id, workflow)
    if "attribute_name" in params:
        attribute_name = params.pop('attribute_name')
        attribute = getattr(user, attribute_name)
        if "attribute_value" in params:
            attribute_value = params.pop('attribute_value')
            return equals(attribute, attribute_value)
    raise ValueError("missing parameter attribute_name or attribute_value")

def object_attribute_filter_exist(workflow, user, object_id, **filter):
    params = parse_parameters(filter, user, object_id, workflow)
    if "attribute_name" in params:
        attribute_name = params.pop('attribute_name')
        object = workflow.object_class().objects.get(id=object_id)
        attribute = getattr(object, attribute_name)
        return attribute.filter(**params).exists()
    else:
        raise ValueError("missing parameter attribute_name")


def user_attribute_filter_exist(workflow, user, object_id, **filter):
    params = parse_parameters(filter, user, object_id, workflow)
    if "attribute_name" in params:
        attribute_name = params.pop('attribute_name')
        attribute = getattr(user, attribute_name)
        return attribute.filter(**params).exists()
    else:
        raise ValueError("missing parameter attribute_name")


def object_filter_exist(workflow, user, object_id, **filter):
    params = parse_parameters(filter, user, object_id, workflow)
    return workflow.object_class().objects.filter(**params).exists()


def user_filter_exist(workflow, user, object_id, **filter):
    params = parse_parameters(filter, user, object_id, workflow)
    return type(user).objects.filter(**params).exists()


def other_filter_exist(workflow, user, object_id, **filter):
    params = parse_parameters(filter, user, object_id, workflow)
    if "model_type" in params:
        model_type = import_from_path(params.pop('model_type'))
        return model_type.objects.filter(**params).exists()
    else:
        raise ValueError("missing parameter model_type")


def parse_parameters(filter, user, object_id, workflow):
    params = dict()
    for k, v in filter.items():
        if v.startswith("{{") and v.endswith("}}"):
            parts = v[2:-2].split(".")
            o = None
            if parts[0] == "user":
                o = user
            elif parts[0] == "object":
                o = workflow.object_class().get(id=object_id)
            else:
                raise ValueError("dynamic parameter values must start with user or object")
            if len(parts) > 1:
                for p in parts[1:]:
                    o = getattr(o, p, None)
                    if o == None:
                        continue
            params.update({k: o})
        else:
            #print("{}: {}".format(k, v))
            params.update({k: v})
    return params