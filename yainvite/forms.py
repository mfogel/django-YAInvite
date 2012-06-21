from django import forms
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Invite, EmailEvent


class SendInviteForm(forms.Form):
    "Form to send an invite"
    email = forms.EmailField()

    def send(self, inviter, domain=None):
        "Create and send an Invite via email"
        email = self.cleaned_data['email']
        domain = domain or Site.objects.get_current().domain
        invite = Invite.objects.create_invite(inviter)

        context = {'domain': domain, 'invite': invite}
        subject = render_to_string('yainvite/email/subject.txt', context)
        subject = ''.join(subject.splitlines()) # must not contain newlines
        message = render_to_string('yainvite/email/body.txt', context)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        EmailEvent.objects.create(invite=invite, domain=domain, sent_to=email)


class RedeemInviteForm(forms.Form):
    "Form to redeem an invite"

    # avoiding re-declaration of 'key' field properties
    key = forms.models.fields_for_model(Invite, fields=['key'])['key']

    def clean_key(self):
        "Verifiy the given key corresponds to an open Invite"
        key = self.cleaned_data['key']
        # Let's provide some semi-helpful error messages
        invite = Invite.objects.get_invite(key)
        if not invite:
            raise forms.ValidationError("Invalid invite key")
        if invite.is_expired():
            raise forms.ValidationError("Invite key expired")
        if invite.is_redeemed():
            raise forms.ValidationError("Invite key has already been redeemed")
        return key

    def redeem(self, user):
        invite = Invite.objects.get_invite(self.cleaned_data['key'])
        invite.redeemer = user
        invite.save()
        return invite
