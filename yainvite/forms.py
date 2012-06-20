from django import forms

from .models import Invite


class SendInviteForm(forms.Form):
    "Form to send an invite"
    email = forms.EmailField()


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
