import base64
import random
import re
import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.formats import localize
from django.utils.hashcompat import sha_constructor

# ensure our default settings get loaded
from .conf import YAInviteConf


class InviteManager(models.Manager):

    # 40 bit base64.b32encode lowered regex
    # http://tools.ietf.org/html/rfc3548.html
    KEY_RE = re.compile('^[a-z2-7]{8}$')

    def is_key_wellformed(self, invite_key):
        "Is the key syntactically valid?"
        return bool(self.KEY_RE.search(invite_key))

    def generate_key(self, inviter):
        """
        Generate a new ``Invite`` key and return it.

        The key for the ``Invite`` will be a SHA1 hash, generated from:
            * time-specific data
            * inviter-specific data
            * a random salt
        """
        payload = ''.join([
            str(timezone.now()),
            str(inviter),
            sha_constructor(str(random.random())).hexdigest(),
        ])
        return base64.b32encode(sha_constructor(payload).digest())[:8].lower()

    def get_invite(self, invite_key):
        """
        Return the ``Invite`` with the given key. Avoid hitting database
        for malformed invite keys.
        """
        if not self.is_key_wellformed(invite_key):
            return None
        try:
            invite = self.get(key=invite_key)
        except self.model.DoesNotExist:
            return None
        return invite

    def create_invite(self, inviter):
        "Create an ``Invite`` and return it"
        key = self.generate_key(inviter)
        return self.create(inviter=inviter, key=key)


class Invite(models.Model):
    key = models.CharField(max_length=8, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        default=lambda: (
            timezone.now() + datetime.timedelta(
                    days=settings.YAINVITE_DEFAULT_LIFETIME)
            if settings.YAINVITE_DEFAULT_LIFETIME
            else None
        ),
        blank=True, null=True,

    )
    inviter = models.ForeignKey(settings.YAINVITE_INVITER_CLASS,
            related_name='invite_created_set')
    redeemer = models.ForeignKey(User, related_name='invite_redeemed_set',
            blank=True, null=True)

    objects = InviteManager()

    def __unicode__(self):
        return u'{}: {}'.format(self.inviter, self.key)

    def is_redeemed(self):
        "Has this Invite been redeemed?"
        return bool(self.redeemer)
    is_redeemed.boolean = True

    def is_expired(self):
        "Has this Invite expired?"
        return timezone.now() > self.expires_at
    is_expired.boolean = True

    def is_open(self):
        "Is this Invite still 'open' - meaning it's unused and unexpired?"
        return not self.is_redeemed() and not self.is_expired()
    is_open.boolean = True


class EmailEvent(models.Model):
    """
    Represents the act of sending an Invite by email using the YAInvite
    tools. Functions as a log of emails sent with invite keys.
    """

    invite = models.ForeignKey(Invite, related_name='emailevent_set')
    domain = models.CharField(max_length=255, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    sent_to = models.EmailField(max_length=255)

    def __unicode__(self):
        return 'To {} at {}'.format(self.sent_to, localize(self.sent_at))
