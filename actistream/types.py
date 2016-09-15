from django.utils import six

from actistream import registry


class ActivityTypeMeta(type):
    def __new__(mcs, name, bases, d):
        userdef = bases[0] != object
        if userdef:
            d['app'] = d['__module__'].split('.')[-2]
            d['code'] = name.lower()
            d['id'] = d['app'] + '.' + d['code']
        ret = type.__new__(mcs, name, bases, d)
        if userdef:
            registry.register(ret)
        return ret


@six.add_metaclass(ActivityTypeMeta)
class ActivityType(object):
    aliases = {}

    @classmethod
    def create(cls, **kwargs):
        from .models import Activity
        commit = kwargs.pop('commit', True)
        activity_kwargs = {}
        for k, v in kwargs.items():
            activity_kwargs[cls.aliases.get(k, k)] = v
        activity = Activity(type=cls.id,
                            **activity_kwargs)
        if commit:
            activity.save()
        return activity


class ActivityWrapper(object):

    def __init__(self, activity):
        self.activity = activity

    def __getattr__(self, name):
        aliases = self.activity.get_type().aliases
        if name in aliases:
            return getattr(self.activity, aliases[name])
        return self.__dict__[name]

    def get_context_data(self):
        return {'activity': self.activity}

    def is_active(self):
        return True
