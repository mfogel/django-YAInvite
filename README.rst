===============
Django YAInvite
===============

Yet Another Invite system for Django. Why another?

-   Supports allocating Invites to a model of your choice - meaning Invites
    don't have to come from a User. If you have multi-user Accounts in your
    project and you'd like associate Invites with those Accounts rather than
    django's default User model, you can.

-   Invites are indexed by key - an 8-character string of lowercase
    letters and numbers. The key is generated from a SHA1 hash of a
    timestamp, invite-allocator specific data and a random salt. 8 characters
    at 5 bits per chacter a total space over 10^12 possible invites keys.

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

#.  Add something like ``(r'^yainvite/', include('yainvite.urls'))`` to your
    project's urls.py.

#.  If desired, adjust some settings. See the configuration section below.
    Note that if you're choosing to allocated and attribute your Invites to
    a model other than the default, you want to configure your
    ``YAINVITE_INVITER_MODEL`` `before` moving on to the next step.

#.  Run the South migration to set up your YAInvite db tables::

        django-admin.py migrate yainvite


Configuration
=============

Available settings:

:``YAINVITE_BACKEND``:
    InviteBackend class to use. The InviteBackend class describes
    how to extract the an ``YAINVITE_INVITER_CLASS`` instance from a
    django http request object, and how to determine how many unused
    invites that instance has available. This should be in standard
    python dotted path format. See ``yainvite/backends.py`` for details.

    Defaults to ``yainvite.backends.UserUnlimitedBackend``.

:``YAINVITE_DEFAULT_LIFETIME``:
    Default number of days an Invite is valid for. Defaults to 7.

:``YAINVITE_INVITER_CLASS``:
    The django model class Invites will be allocated to and sent from. This
    does not change how Invites are redeemed - they're always redeemed by
    a User signing up at the site. This should be in ``app_name.ModelName``
    format.

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

:``YAINVITE_REDIRECT_NEW_USER_TO``:
    Name of url to redirect new user to after they've redeemed their
    invite.

    Defaults to ``yainvite_redeemed``

:``YAINVITE_USER_AUTO_LOGIN``:
    Should we automatically log the user in after they redeem an invite?

    Defaults to False.


Dependencies
============

- `South`__ for data migration, support of flexible ForeignKey allocating
  Invites to a model of your choosing.

- `django-appconf`__ for sane django app configuration/settings.

- `django-extra-views`__ for helpful multi-form View handling.


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
__ https://github.com/AndrewIngram/django-extra-views
__ https://github.com/mfogel/django-YAInvite
__ http://code.larlet.fr/django-invitation/overview
