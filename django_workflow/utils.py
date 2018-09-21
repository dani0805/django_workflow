from collections import OrderedDict
import re

import six
import json

from graphql_relay import from_global_id


def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)


def import_from_path(full_path):
    parts = full_path.rsplit(".", 1)
    return import_from(parts[0], parts[1])


_first_cap_re = re.compile('(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')

def camelcase_to_underscore(word):
    """
    Needed to replicate the transformation between capitalize convention (graph-ql) and underscore convention (python)
    :param word:
    :return:
    """
    s1 = _first_cap_re.sub(r'\1_\2', word)
    return _all_cap_re.sub(r'\1_\2', s1).lower()


def parse_global_ids(return_node_types=None, include_branches=None):
    def decorator(func, **kwargs):
        def decorated_function(cls, root, info , **data):
            node_types = dict()
            current_dict = data
            parse_branch(current_dict, data, node_types, list())
            return func(cls, root, info , node_types=node_types, **data)

        def parse_branch(current_dict, data, node_types, route):
            if isinstance(current_dict, dict) or isinstance(current_dict, OrderedDict):
                normalized_key_values = dict()
                for key, value in current_dict.items():
                    # if key.endswith("Id"):
                    key = camelcase_to_underscore(key)
                    normalized_key_values[key] = value
                current_dict.update(normalized_key_values)
                for key, value in current_dict.items():
                    if key.endswith("_id"):
                        parse_node(data, key, node_types, route)
                    if include_branches is not None and key in include_branches:
                        this_dict = from_string(current_dict, key)
                        parse_branch(this_dict, data, node_types, route + [key,])
            elif isinstance(current_dict, list) or isinstance(current_dict, tuple):
                for i, this_dict in enumerate(current_dict):
                    this_dict = from_string(current_dict, i)
                    parse_branch(this_dict, data, node_types, route + [i, ])
            else:
                raise ValueError("invalid type {}".format(type(current_dict)))

        def from_string(current_dict, key):
            this_dict = current_dict[key]
            if isinstance(this_dict, six.string_types):
                this_dict = json.loads(this_dict)
                current_dict[key] = this_dict
            return this_dict

        def parse_node(data, key, node_types, route):
            this_dict = data
            node_type = None
            for node in route:
                this_dict = this_dict[node]
            try:
                try_parse = json.loads(this_dict[key])
                if isinstance(try_parse, list) or isinstance(try_parse, tuple):
                    val = [from_global_id(x)[1] for x in try_parse]
                    this_dict[key] = val
            except:
                try:
                    node_type, this_dict[key] = from_global_id(this_dict[key])
                except:
                    pass
            if return_node_types is not None and key in return_node_types and not route:
                node_types.update({key: node_type})

        return decorated_function
    return decorator
