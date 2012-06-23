"""
Tests for django-YAInvite
"""

from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core import mail
from django.core import management
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import TestCase
from django.utils import timezone

from .backends import SiteBackend, UserUnlimitedBackend
from .forms import RedeemInviteForm, SendInviteForm
from .models import Invite


class InviteModelTestCase(TestCase):
    """
    Test the Invite model.
    """

    def setUp(self):
        self.inviter = User.objects.create(
                username='user1', password='-', email='user1@example.com')
        self.redeemer = User.objects.create(
                username='user2', password='-', email='user2@example.com')
        self.invite1 = Invite.objects.create_invite(self.inviter)
        self.invite2 = Invite.objects.create_invite(self.inviter)
        self.invite3 = Invite.objects.create_invite(self.inviter)

    def test_created(self):
        self.assertEqual(self.invite1, Invite.objects.order_by('id')[:1].get())
        self.assertEqual(3, Invite.objects.count())

    def test_get_by_key(self):
        invite1 = Invite.objects.get_invite(self.invite1.key)
        self.assertEqual(invite1, self.invite1)

    def test_wellformed_keys(self):
        self.assertTrue(Invite.objects.is_key_wellformed(self.invite1.key))
        self.assertTrue(Invite.objects.is_key_wellformed(self.invite2.key))
        self.assertTrue(Invite.objects.is_key_wellformed(self.invite3.key))

    def test_redeem(self):
        self.assertFalse(self.invite1.is_redeemed())
        self.invite1.redeemer = self.redeemer
        self.assertTrue(self.invite1.is_redeemed())

    def test_expire(self):
        self.assertFalse(self.invite1.is_expired())
        self.invite1.expires_at = timezone.now() - timedelta.resolution
        self.assertTrue(self.invite1.is_expired())

    def test_open(self):
        self.assertTrue(self.invite1.is_open())
        self.invite1.redeemer = self.redeemer
        self.assertFalse(self.invite1.is_open())

        self.assertTrue(self.invite2.is_open())
        self.invite2.expires_at = timezone.now() - timedelta.resolution
        self.assertFalse(self.invite2.is_open())

    def test_key_generation(self):
        # it's hard to test key generation is uniformly randomly
        # distributed across the space
        key1 = Invite.objects.generate_key(self.inviter)
        self.assertIsInstance(key1, basestring)
        self.assertEqual(len(key1), 8)

        key2 = Invite.objects.generate_key(self.inviter)
        self.assertNotEqual(key1, key2)


class RedeemInviteFormTestCase(TestCase):
    """
    Test the RedeemInviteForm
    """

    def setUp(self):
        self.inviter = User.objects.create(
                username='user', password='-', email='user@example.com')
        self.redeemer = User.objects.create(
                username='redeemer', password='-',
                email='redeemer@example.com')
        self.invite = Invite.objects.create_invite(self.inviter)

    def test_redeem_open(self):
        form = RedeemInviteForm({'key': self.invite.key})
        self.assertTrue(form.is_valid())

    def test_redeem_redeemed_already(self):
        self.invite.redeemer = self.inviter
        self.invite.save()
        form = RedeemInviteForm({'key': self.invite.key})
        self.assertFalse(form.is_valid())

    def test_redeem_expired_already(self):
        self.invite.expires_at = timezone.now() - timedelta.resolution
        self.invite.save()
        form = RedeemInviteForm({'key': self.invite.key})
        self.assertFalse(form.is_valid())

    def test_invalid_keys(self):
        self.assertFalse(RedeemInviteForm().is_valid())
        self.assertFalse(RedeemInviteForm({'key': ''}).is_valid())
        self.assertFalse(RedeemInviteForm({'key': 'beefcake'}).is_valid())


class SendInviteFormTestCase(TestCase):
    """
    Test the SendInviteForm
    """

    to_addr = 'test@example.com'

    def setUp(self):
        self.inviter = User.objects.create(
                username='user', password='-', email='user@example.com')

    def test_form_valid(self):
        self.assertFalse(SendInviteForm().is_valid())
        form = SendInviteForm({'email': self.to_addr})
        self.assertTrue(form.is_valid())

    def test_send_email(self):
        form = SendInviteForm({'email': 'test@example.com'})
        form.full_clean()
        form.send(self.inviter)
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(len(msg.to), 1)
        self.assertEqual(msg.to[0], self.to_addr)


class SiteBackendTestCase(TestCase):
    """
    Test the SiteBackend
    """

    def setUp(self):
        request = HttpRequest()
        self.backend = SiteBackend(request)

    def test_unlimited(self):
        self.assertGreater(self.backend.number_invites_remaining, 0)
        self.backend.number_invites_remaining = 0
        self.assertGreater(self.backend.number_invites_remaining, 0)

    def test_site(self):
        self.assertEqual(self.backend.inviter, Site.objects.get_current())


class UserUnlimitedBackendTestCase(TestCase):
    """
    Test the SiteBackend
    """

    def setUp(self):
        self.user = User.objects.create(
                username='user', password='-', email='user@example.com')
        request = HttpRequest()
        request.user = self.user
        self.backend = UserUnlimitedBackend(request)

    def test_unlimited(self):
        self.assertGreater(self.backend.number_invites_remaining, 0)
        self.backend.number_invites_remaining = 0
        self.assertGreater(self.backend.number_invites_remaining, 0)

    def test_user(self):
        self.assertEqual(self.backend.inviter, self.user)


class UserProfileBackendTestCase(TestCase):
    # TODO: fill me in
    pass


class FunctionalTestCase(TestCase):
    """
    Test the send-redeem invite process from perspective of an
    external client.
    """
    # TODO: fill me in
    pass
