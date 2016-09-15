from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail

from actistream.models import Notice

from . import activities
from .models import Comment, Article


User = get_user_model()


class ActivityTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='john@doe.com',
            username='john')

    def test_comment_posted(self):
        article = Article.objects.create()
        comment = Comment.objects.create(
            article=article,
            user=self.user)
        activity = activities.CommentPosted.create(
            target=article,
            actor=self.user,
            action_object=comment)
        notice_recipients = [self.user]
        Notice.objects.send(
            activity,
            notice_recipients)
        msg = mail.outbox[0]
        self.assertEquals(msg.subject, 'Comment posted')
        assert msg.to == ['john@doe.com']
        assert msg.content_subtype == 'html'

