=============================
Welcome to django-actistream!
=============================

.. image:: https://badge.fury.io/py/django-actistream.png
   :target: http://badge.fury.io/py/django-actistream

.. image:: https://travis-ci.org/pennersr/django-actistream.png
   :target: http://travis-ci.org/pennersr/django-actistream

.. image:: https://img.shields.io/pypi/v/django-actistream.svg
   :target: https://pypi.python.org/pypi/django-actistream

.. image:: https://coveralls.io/repos/pennersr/django-actistream/badge.png?branch=master
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

- *John* (=the actor) has *posted a comment* (=the activity type) stating *"I don't get it!"* (=the action object) on the article titled *"actistream for dummies"* (the target).

A notice is an action addressed to a user. So, in Jane's inbox you may want to display that John posted that comment. For that purpose, create a ``Notice`` relating the above activity to Jane.

Status
======

Running in production since 2012, released as open source in september 2016.
