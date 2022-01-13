try:
    import importlib
except ImportError:
    from django.utils import importlib  # noqa


def import_attribute(path):
    pkg, attr = path.rsplit('.', 1)
    ret = getattr(importlib.import_module(pkg), attr)
    return ret
