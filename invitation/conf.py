from django.conf import settings
from appconf import AppConf


class InvitationConf(AppConf):
    # number of days an invitation is valid for
    INVITE_LIFETIME = 7

    # number of invites granted to each new user
    INVITES_PER_USER = 0
