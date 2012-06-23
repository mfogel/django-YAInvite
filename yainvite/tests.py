"""
Tests for django-YAInvite
"""

from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core import management
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Invite


class InviteModelTestCase(TestCase):
    """
    Test the Invite model.
    """

    def setUp(self):
        self.inviter = User.objects.create(
                username='user1', password='pass1', email='user1@example.com')
        self.redeemer = User.objects.create(
                username='user2', password='pass2', email='user2@example.com')
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
