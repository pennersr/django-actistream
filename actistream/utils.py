from django.utils import six

try:
    import importlib
except ImportError:
    from django.utils import importlib  # noqa


def import_attribute(path):
    assert isinstance(path, six.string_types)
    pkg, attr = path.rsplit('.', 1)
    ret = getattr(importlib.import_module(pkg), attr)
    return ret
