from django import forms

class SendInviteForm(forms.Form):
    "Form to send an invite"
    email = forms.EmailField()
