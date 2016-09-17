from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail

from actistream.models import Notice, Activity

from . import activities
from .models import Comment, Article


User = get_user_model()


class ActivityTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='john@doe.com',
            username='john')
        self.article = Article.objects.create()
        self.comment = Comment.objects.create(
            article=self.article,
            user=self.user)
        self.activity = activities.CommentPosted.create(
            target=self.article,
            actor=self.user,
            action_object=self.comment)

    def test_notice(self):
        notice_recipients = [self.user]
        Notice.objects.send(
            self.activity,
            notice_recipients)
        msg = mail.outbox[0]
        self.assertEquals(msg.subject, 'Comment posted')
        assert msg.to == ['john@doe.com']
        assert msg.content_subtype == 'html'

    def test_for_target(self):
        qs = Activity.objects.for_target(self.article)
        assert qs.count() == 1
        assert qs.filter(pk=self.activity.pk).exists()

    def test_for_action_object(self):
        qs = Activity.objects.for_action_object(self.comment)
        assert qs.count() == 1
        assert qs.filter(pk=self.activity.pk).exists()

    def test_for_action_objects(self):
        qs = Activity.objects.for_action_objects(
            Comment.objects.all())
        assert qs.count() == 1
        assert qs.filter(pk=self.activity.pk).exists()

    def test_fetch_related(self):
        # TODO: Actually test something
        Activity.objects.fetch_related(Activity.objects.all())
