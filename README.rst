===============
Django YAInvite
===============

Yet Another Invite system for Django. Why another?

-   Supports allocating Invites to a model of your choice - meaning Invites
    don't have to come from a User. If you have multi-user Accounts in your
    project and you'd like associate Invites with those Accounts rather than
    django's default User model, you can.

-   Invites are indexed by key - a SHA1 hash of a timestamp, invite-allocator
    specific data and a salt. This key can be passed around in any form,
    ie. you can print these Invites out and go door-to-door with them if
    you so desire.

-   Invite-specifc expiration dates. You configure a default lifetime for
    invites, but then can specifically edit the expiration dates on a
    per-invite basis.

-   Invites are redeemed via the signup of a new auth.User. Each invite
    may only be redeemed once.


Installation
============

#.  Until this is on pypi, you can install from source::

        pip install -e git://github.com/mfogel/django-YAInvite.git

#.  Add ``yainvite`` to your ``INSTALLED_APPS``.

#.  If desired, adjust some settings. See the configuration section below.
    Note that if you're choosing to allocated and attribute your Invites to
    a model other than the default, you want to configure your
    ``YAINVITE_INVITER_MODEL`` `before` moving on to the next step.

#.  Run the South migration to set up your YAInvite db tables::

        django-admin.py migrate yainvite


Configuration
=============

Available settings:

:``YAINVITE_DEFAULT_LIFETIME``:
    Default number of days an Invite is valid for. Defaults to 7.

:``YAINVITE_BACKEND``:
    InviteBackend class to use. The InviteBackend class describes
    how to extract the an ``YAINVITE_INVITER_CLASS`` instance from a
    django http request object, and how to determine how many unused
    invites that instance has available. See ``yainvite/backends.py``
    for details.

    Defaults to ``yainvite.backends.UserUnlimitedBackend``.

:``YAINVITE_INVITER_CLASS``:
    The django model class Invites will be allocated to and sent from. This
    does not change how Invites are redeemed - they're always redeemed by
    a User signing up at the site.

    Defaults to ``auth.User``.

:``YAINVITE_INVITER_DB_TABLE``:
    If your ``YAINVITE_INVITER_CLASS`` is set to a model that has a custom
    db_table name set in it's Meta, then you need to define this to
    match. Elsewise, there's no need to configure this.

:``YAINVITE_USER_CREATION_FORM``:
    Form class to use to create a new User when redeeming an invite.
    Required to have a save() method. This should be in standard python
    dotted path format.

    Defaults to ``django.contrib.auth.forms.UserCreationForm``


Dependencies
============

- `South`__ for data migration, support of flexible ForeignKey allocating
  Invites to a model of your choosing.

- `AppConf`__ for sane django app configuration/settings.


Found a Bug?
============

To file a bug of submit a patch, please head over to the
`django-YAInvite repository`__. Bug reports are welcome, especially if they
come with tests that demonstrate the failure ;)


Credits
=======

Originally adapted from `David Larlet's django-invitation`__.


__ http://south.aeracode.org/
__ https://github.com/jezdez/django-appconf
__ https://github.com/mfogel/django-YAInvite
__ http://code.larlet.fr/django-invitation/overview