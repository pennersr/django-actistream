from django.template import Library
from django.template.loader import render_to_string

from ..models import Activity

register = Library()


@register.simple_tag(takes_context=True)
def render_activity(context, activity):
    activity_type = activity.get_type()
    data = activity.wrapper().get_context_data()
    return render_to_string('{0}/activities/{1}_detail.html'
                            .format(activity_type.app,
                                    activity_type.code),
                            data,
                            context)


@register.assignment_tag
def renderable_activities(activities):
    a = Activity.objects.fetch_related(activities)
    return Activity.objects.filter_active(a)
