from importlib import import_module

VERSION = (1, 0, 5, 'final', 0)

__title__ = 'django-actistream'
__version_info__ = VERSION
__version__ = '.'.join(map(str, VERSION[:3])) + ('-{}{}'.format(
    VERSION[3], VERSION[4] or '') if VERSION[3] != 'final' else '')
__author__ = 'Raymond Penners'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Raymond Penners and contributors'


class ActivityTypeRegistry(object):
    def __init__(self):
        self.type_map = {}

    def get_list(self):
        return self.type_map.values()

    def register(self, cls):
        self.type_map[cls.id] = cls()

    def by_id(self, id):
        return self.type_map[id]

    def as_choices(self):
        for nt in self.get_list():
            yield (nt.id, nt.verbose_name)

    def load(self):
        from django.conf import settings
        for app in settings.INSTALLED_APPS:
            try:
                m = app + '.activities'
                import_module(m)
            except ImportError:
                pass


registry = ActivityTypeRegistry()
