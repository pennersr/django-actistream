from __future__ import absolute_import

from collections import defaultdict

from django.conf import settings
from django.db import models
from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible

from actistream import registry


class ActivityManager(models.Manager):

    def _filter_flags(self, qs, flags):
        if flags:
            qry = None
            for mask in flags:
                q = Q(**{'flags': F('flags').bitor(mask)})
                if not qry:
                    qry = q
                else:
                    qry = qry | q
            qs = qs.filter(qry)
        return qs

    def for_action_objects(self, action_objects):
        ct = ContentType.objects.get_for_model(action_objects.model)
        activities = Activity.objects \
            .filter(action_object_ct=ct,
                    action_object_id__in=action_objects.values_list(
                        'id',
                        flat=True))
        return activities

    def for_action_object(self, action_object):
        ct = ContentType.objects.get_for_model(action_object)
        activities = Activity.objects \
            .filter(action_object_ct=ct,
                    action_object_id=action_object.pk)
        return activities

    def for_target(self, target, types=None, flags=None):
        """
        flags: [1, 2, 12] == 1 or 2 or (8 and 4)
        """
        ct = ContentType.objects.get_for_model(target)
        activities = Activity.objects \
            .filter(target_ct=ct,
                    target_id=target.pk)
        if types:
            activities = activities.filter(type__in=[t.id for t in types])
        if flags:
            activities = self._filter_flags(activities, flags)
        return activities.order_by('-created_at')

    def fetch_related(self, qs):
        """
        Excludes activities with incomplete (deleted) relations
        """
        ct_to_obj_ids = defaultdict(set)
        fields = ['actor', 'target', 'action_object']
        # Collect objects to fetch
        for activity in qs:
            for field in fields:
                ct_id = getattr(activity, field + '_ct_id')
                obj_id = getattr(activity, field + '_id')
                if ct_id and obj_id:
                    ct_to_obj_ids[ct_id].add(obj_id)
        # Fetch objects
        ct_to_obj_id_to_obj = {}
        for ct_id, obj_ids in ct_to_obj_ids.items():
            ct = ContentType.objects.get_for_id(ct_id)
            model = ct.model_class()
            objs = model.objects.filter(id__in=obj_ids)
            ct_to_obj_id_to_obj[ct_id] = dict([(o.pk, o) for o in objs])
        # Put objects back in activity
        ret = []
        for activity in qs:
            try:
                for field in fields:
                    ct_id = getattr(activity, field + '_ct_id')
                    obj_id = getattr(activity, field + '_id')
                    if ct_id and obj_id:
                        obj = ct_to_obj_id_to_obj[ct_id].get(obj_id)
                        if not obj:
                            raise ObjectDoesNotExist
                        setattr(activity, field, obj)
                ret.append(activity)
            except ObjectDoesNotExist:
                pass
        return ret

    def filter_active(self, activities):
        """
        activities = list, not a queryset
        """
        ret = []
        for activity in activities:
            if activity.wrapper().is_active():
                ret.append(activity)
        return ret


@python_2_unicode_compatible
class Activity(models.Model):
    objects = ActivityManager()

    actor_ct = models.ForeignKey(ContentType, related_name='+',
                                 blank=True, null=True)
    actor_id = models.PositiveIntegerField()
    actor = GenericForeignKey('actor_ct', 'actor_id')

    target_ct = models.ForeignKey(ContentType, related_name='+',
                                  blank=True, null=True)
    target_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_ct', 'target_id')

    action_object_ct = models.ForeignKey(ContentType, related_name='+',
                                         blank=True, null=True)
    action_object_id = models.PositiveIntegerField()
    action_object = GenericForeignKey(
        'action_object_ct',
        'action_object_id')
    type = models.CharField(max_length=100,
                            choices=registry.as_choices(),
                            verbose_name=_("type"))
    flags = models.BigIntegerField(default=0)  # Project specific flags
    extra_data = models.TextField(
        _("additional data"),
        blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')

    def get_type(self):
        activity_type = registry.by_id(self.type)
        return activity_type

    def wrapper(self):
        return self.get_type().Wrapper(self)

    def __str__(self):
        return self.type


class NoticeManager(models.Manager):

    def send(self, activity, users, request=None):
        for user in users:
            notice = Notice.objects.create(
                user=user,
                activity=activity,
                created_at=activity.created_at)
            activity.wrapper().send_notice_mail(notice, request)


class Notice(models.Model):
    objects = NoticeManager()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='+',
        verbose_name=_("user"))
    activity = models.ForeignKey(Activity)
    # Denormalized.. matches activity
    created_at = models.DateTimeField(_('created at'))
    read_at = models.DateTimeField(_("read at"), blank=True, null=True)
    archived_at = models.DateTimeField(_("archived at"), blank=True, null=True)

    class Meta:
        verbose_name = _('notice')
        verbose_name_plural = _('notices')
        index_together = [
            ['user', 'read_at']
        ]

registry.load()
