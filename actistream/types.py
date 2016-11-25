import json
from django.utils import six

from actistream import registry
from .adapter import get_adapter


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

    def get_user_email(self, user):
        return user.email

    def get_notice_mail_context_data(self, notice, request=None):
        return {
            'activity': self.activity,
            'activity_context':
            self.get_context_data(),
            'notice': notice,
            'user': notice.user}

    def render_notice_mail(self, notice, request=None):
        ctx = self.get_notice_mail_context_data(notice, request)
        activity_type = self.activity.get_type()
        return get_adapter(request).render_mail(
            '{0}/activities/{1}'
            .format(activity_type.app,
                    activity_type.code),
            self.get_user_email(notice.user),
            context=ctx)

    def send_notice_mail(self, notice, request=None):
        msg = self.render_notice_mail(notice, request)
        msg.send()
        return msg


@six.add_metaclass(ActivityTypeMeta)
class ActivityType(object):
    aliases = {}
    Wrapper = ActivityWrapper

    @classmethod
    def create(cls, **kwargs):
        from .models import Activity
        commit = kwargs.pop('commit', True)
        activity_kwargs = {}
        for k, v in kwargs.items():
            activity_kwargs[cls.aliases.get(k, k)] = v
        extra_data = activity_kwargs.get('extra_data')
        if extra_data is not None and not isinstance(
                extra_data, six.string_types):
            activity_kwargs['extra_data'] = json.dumps(extra_data)
        activity = Activity(type=cls.id,
                            **activity_kwargs)
        if commit:
            activity.save()
        return activity
