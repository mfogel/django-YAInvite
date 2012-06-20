import random
import re
import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.formats import localize
from django.utils.hashcompat import sha_constructor

# ensure our default settings get loaded
from .conf import YAInviteConf


# from django-registration
SHA1_RE = re.compile('^[a-f0-9]{40}$')


class InviteManager(models.Manager):

    def is_key_wellformed(self, invite_key):
        "Is the key syntactically valid?"
        return bool(SHA1_RE.search(invite_key))

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
        """
        Create an ``Invite`` and return it.

        The key for the ``Invite`` will be a SHA1 hash, generated from:
            * time-specific data
            * inviter-specific data
            * a random salt
        """
        payload = ''.join([
            str(timezone.now()),
            str(inviter),
            sha_constructor(str(random.random())).hexdigest()[:5],
        ])
        key = sha_constructor(payload).hexdigest()
        return self.create(inviter=inviter, key=key)


class Invite(models.Model):
    key = models.CharField(max_length=40, db_index=True)
    invited = models.DateTimeField(default=timezone.now)
    expires = models.DateTimeField(
        default=lambda: (
            timezone.now() + datetime.timedelta(
                    days=settings.YAINVITE_DEFAULT_LIFETIME)
            if settings.YAINVITE_DEFAULT_LIFETIME
            else None
        ),
        blank=True, null=True,

    )
    inviter = models.ForeignKey(settings.YAINVITE_INVITER_CLASS,
            related_name='invite_sent_set')
    redeemer = models.ForeignKey(User, related_name='invite_redeemed_set',
            blank=True, null=True)

    objects = InviteManager()

    def __unicode__(self):
        return u'From {} at {}'.format(self.inviter, localize(self.invited))

    def is_redeemed(self):
        "Has this Invite been redeemed?"
        return bool(self.redeemer)
    is_redeemed.boolean = True

    def is_expired(self):
        "Has this Invite expired?"
        return timezone.now() > self.expires
    is_expired.boolean = True

    def is_open(self):
        "Is this Invite still 'open' - meaning it's unused and unexpired?"
        return not self.is_redeemed() and not self.is_expired()
    is_open.boolean = True

    def send_to(self, email, domain=None):
        """
        Send an invite email to ``email``.
        """
        context = {
            'domain': domain or Site.objects.get_current().domain,
            'invite': self,
        }

        subject = render_to_string('yainvite/email/subject.txt', context)
        subject = ''.join(subject.splitlines()) # must not contain newlines

        message = render_to_string('yainvite/email/body.txt', context)

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
