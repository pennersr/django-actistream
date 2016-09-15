from actistream.types import ActivityWrapper, ActivityType


class CommentPosted(ActivityType):
    verbose_name = 'Comment posted'

    class Wrapper(ActivityWrapper):

        def get_action_url(self):
            return self.activity.action_object.get_absolute_url()
