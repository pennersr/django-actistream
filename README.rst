=============================
Welcome to django-actistream!
=============================

.. image:: https://badge.fury.io/py/django-actistream.png
   :target: http://badge.fury.io/py/django-actistream

.. image:: https://github.com/pennersr/django-actistream/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/pennersr/django-actistream/actions

.. image:: https://img.shields.io/pypi/v/django-actistream.svg
   :target: https://pypi.python.org/pypi/django-actistream

.. image:: https://coveralls.io/repos/pennersr/django-actistream/badge.png?branch=main&_
   :alt: Coverage Status
   :target: https://coveralls.io/r/pennersr/django-actistream

.. image:: https://pennersr.github.io/img/bitcoin-badge.svg
   :target: https://blockchain.info/address/1AJXuBMPHkaDCNX2rwAy34bGgs7hmrePEr

Small core for dealing with activities & notifications.

Source code
  http://github.com/pennersr/django-actistream


Rationale
=========

There are quite some Django apps for dealing with activities & notifications,
yet none match my expectations/requirements:

- Action URLs: they do not belong in the database/models, as your database
  records will outlive the URL routing configuration.

- Texts & descriptions: these neither belong in the database/models. If you need to change
  the wording or correct a typ-o, you should not have to go over all existing records to
  make the change as well. But more importantly, you need to cater for internationalization,
  so these belong in templates where e.g. ``{% blocktrans %}`` can be used. 

- Views: any views that are offered out of the box are not going to match your requirements,
  and won't fit in with your single page application.

- Project specific data: `actistream` allows for storing additional project
  specific data per activity, and flagging activities in a performant manner.

Concepts
========

An activity is about an actor, involved in an action of a certain activity type, relating an action object to a target. For example:

- *John* (=the actor) has *posted a comment* (=the activity type) stating *"I don't get it!"* (=the action object) on the blog post titled *"actistream for dummies"* (the target).

A notice is an action addressed to a user. So, in Jane's inbox you may want to display that John posted that comment. For that purpose, create a ``Notice`` relating the above activity to Jane.

Quick Start
===========

Suppose you have a an app called ``blog`` dealing with posts and comments.
Create a file named ``blog/activities.py``, containing::

    from actistream.types import ActivityWrapper, ActivityType
    
    class CommentPosted(ActivityType):
        verbose_name = 'Comment posted'
    
        class Wrapper(ActivityWrapper):
            """
            Wraps the generic ``Activity`` model, expose any helper methods
            you see fit. Notice that the action URL is not stored in the 
            database.
            """

            def get_action_url(self):
                return self.activity.action_object.get_absolute_url()
    
            def is_active(self):
                """
                Completely optional, but just to show that it handles
                the case where things get deleted.
                """
                comment = self.activity.action_object
                return not comment.post.is_deleted


Given the above, whenever a new comment is created, do::

    from blog.activities import CommentPosted

    def some_view(request):
        ...
        activity = CommentPosted.create(
            target=post,  # The post that gets commented
            actor=self.request.user,
            action_object=comment,  # The newly posted comment
        )

To notice users about this activity, do::

    from actistream.models import Notice

    notice_recipients = User.objects.filter(...)
    Notice.objects.send(
        activity,
        notice_recipients)

Notices need to be turned into emails. For that purpose you'll need to setup a few templates::

    blog/activities/commentposted_subject.txt
    blog/activities/commentposted_message.txt
    blog/activities/commentposted_message.html

Only one of ``.txt`` or ``.html`` is required, both are allowed for combined
text and HTML mails.

For turning an activity into an HTML snippet, e.g. to be displayed in a feed, do::

    {% load actistream %}
    {% render_activity activity %}

This will try to find a template named::

    blog/activities/commentposted_detail.html

Which could look someting like::

    {{ activity.actor }} posted a comment to
    <a href="{{activity.wrapper.get_action_url}}">{{ activity.action_object.post }}</a>.


Status
======

Running in production since 2012, released as open source in september 2016.
