# ConfApp recommends importing settings in this file, doesn't say why
# https://github.com/jezdez/django-appconf/blob/develop/README.rst
from django.conf import settings

from appconf import AppConf


class InvitationConf(AppConf):
    # number of days an invitation is valid for
    INVITE_LIFETIME = 7

    # number of invites granted to each new user
    INVITES_PER_USER = 0

    # Backend class to use
    BACKEND = 'invitation.backends.UserProfileBackend'
    #BACKEND = 'invitation.backends.SiteBackend'

    # What the Invite object should link to. Probably also where you
    # want to keep track of 'number_invites_remaining'
    INVITOR_CLASS = 'auth.User'
    #INVITOR_CLASS = 'sites.Site'

    # If your INVITOR_CLASS has a special db table named in it's Meta,
    # that needs to be replicated here
    INVITOR_DB_TABLE = INVITOR_CLASS.lower().replace('.', '_')
    #INVITOR_DB_TABLE = 'django_site'
