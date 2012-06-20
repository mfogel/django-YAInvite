# ConfApp recommends importing settings in this file, doesn't say why
# https://github.com/jezdez/django-appconf/blob/develop/README.rst
from django.conf import settings
from appconf import AppConf


class YAInviteConf(AppConf):
    # number of days an invite is valid for
    DEFAULT_LIFETIME = 7

    # Backend class to use
    BACKEND = 'yainvite.backends.UserUnlimitedBackend'

    # What the Invite object should link to. Probably also where you
    # want to keep track of 'number_invites_remaining'
    INVITER_CLASS = 'auth.User'

    # If your INVITER_CLASS has a special db table named in it's Meta,
    # that needs to be replicated here
    INVITER_DB_TABLE = INVITER_CLASS.lower().replace('.', '_')
