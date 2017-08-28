def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)


def import_from_path(full_path):
    parts = full_path.rsplit(".", 1)
    return import_from(parts[0], parts[1])