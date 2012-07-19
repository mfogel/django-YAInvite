# ConfApp recommends importing settings in this file, doesn't say why
# https://github.com/jezdez/django-appconf/blob/develop/README.rst
from django.conf import settings
from django.db import connection
from django.db.backends.util import truncate_name
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
    INVITER_DB_TABLE = None

    # form class to use when redeeming an Invite
    USER_CREATION_FORM = 'yainvite.forms.UserCreationForm'

    # name of url to redirect new user to after they've redeemed their invite
    REDIRECT_NEW_USER_TO = 'yainvite_redeemed'

    def configure(self):
        data = self.configured_data
        if not data['INVITER_DB_TABLE']:
            # from: django/db/models/options.py#L112 (django 1.4)
            app, module = data['INVITER_CLASS'].lower().split('.')
            db_table_long = '{}_{}'.format(app, module)
            data['INVITER_DB_TABLE'] = truncate_name(
                    db_table_long, connection.ops.max_name_length())
        return data
