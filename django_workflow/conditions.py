# import a definition from a module at runtime
from django.db.models.manager import Manager

from django_workflow.utils import import_from, import_from_path


def object_attribute_filter_exist(workflow, object_id, user, **filter):
    params = parse_parameters(filter, object_id, user, workflow)
    if "attribute_name" in params:
        attribute_name = params.pop('model_type')
        object = workflow.object_class().objects.get(id=object_id)
        attribute = getattr(object, attribute_name)
        return attribute.filter(**params).exists()
    else:
        raise ValueError("missing parameter attribute_name")


def user_attribute_filter_exist(workflow, object_id, user, **filter):
    params = parse_parameters(filter, object_id, user, workflow)
    if "attribute_name" in params:
        attribute_name = params.pop('model_type')
        attribute = getattr(user, attribute_name)
        return attribute.filter(**params).exists()
    else:
        raise ValueError("missing parameter attribute_name")


def object_filter_exist(workflow, object_id, user, **filter):
    params = parse_parameters(filter, object_id, user, workflow)
    return workflow.object_class().objects.filter(**params).exists()


def user_filter_exist(workflow, object_id, user, **filter):
    params = parse_parameters(filter, object_id, user, workflow)
    return type(user).objects.filter(**params).exists()


def other_filter_exist(workflow, object_id, user, **filter):
    params = parse_parameters(filter, object_id, user, workflow)
    if "model_type" in params:
        model_type = import_from_path(params.pop('model_type'))
        return model_type.objects.filter(**params).exists()
    else:
        raise ValueError("missing parameter model_type")


def parse_parameters(filter, object_id, user, workflow):
    params = dict()
    for k, v in filter.items():
        if v.startswith("{") and v.endswith("}"):
            parts = v[1:-1].split(".")
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
            params.update({k, o})
        else:
            params.update({k, v})
    return params