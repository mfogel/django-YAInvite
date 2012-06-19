from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from invitation.models import InvitationKey
from invitation.forms import SendInviteForm


class LoginRequiredMixin(object):
    "Restrict a View to only logged-in Users"
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class SendInviteView(LoginRequiredMixin, FormView):
    "Send an invite"
    form_class = SendInviteForm
    template_name = 'invitation/send.html'
    success_url = reverse_lazy('invitation_sent')

    def get_context_data(self, **kwargs):
        context = super(SendInviteView, self).get_context_data(**kwargs)
        context['remaining_invitations'] = (
            InvitationKey.objects.remaining_invitations_for_user(self.request.user)
        )
        return context

    def form_valid(self, form):
        "Send the invite"
        invitation = InvitationKey.objects.create_invitation(self.request.user)
        invitation.send_to(form.cleaned_data['email'])
        return super(SendInviteView, self).form_valid(form)


class InviteSentView(LoginRequiredMixin, TemplateView):
    "Invite successfully sent - success page"
    template_name = 'invitation/sent.html'


class RedeemInviteView(FormView):
    "Redeem an invite"
    form_class = UserCreationForm
    template_name = 'invitation/redeem.html'
    success_url = reverse_lazy('invitation_redeemed')

    @property
    def invitation_key(self):
        return self.kwargs.get('invitation_key')

    @property
    def is_key_valid(self):
        return InvitationKey.objects.is_key_valid(self.invitation_key)

    def get_context_data(self, **kwargs):
        context = super(RedeemInviteView, self).get_context_data(**kwargs)
        context.update({
            'invitation_key': self.invitation_key,
            'is_valid': self.is_key_valid,
        })
        return context

    def form_valid(self, form):
        "Redeem the invite"
        if not self.is_key_valid:
            return super(RedeemInviteView, self).form_invalid(form)
        new_user = form.save()
        invitation = InvitationKey.objects.get(key=self.invitation_key)
        invitation.mark_used(new_user)
        return super(RedeemInviteView, self).form_valid(form)


class InviteRedeemedView(TemplateView):
    "Invite successfully redeemed - success page"
    template_name = 'invitation/redeemed.html'
