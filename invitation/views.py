from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from invitation.models import InvitationKey
from invitation.forms import InvitationKeyForm


class LoginRequiredMixin(object):
    "Restrict a View to only logged-in Users"
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class SendInviteView(LoginRequiredMixin, FormView):
    "Send an invite"
    form_class = InvitationKeyForm
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


class RedeemInviteView(TemplateView):
    "Redeem an invite"
    template_name = 'invitation/redeem.html'

    def get_context_data(self, **kwargs):
        context = super(RedeemInviteView, self).get_context_data(**kwargs)
        invitation_key = self.kwargs.get('invitation_key')
        context.update({
            'invitation_key': invitation_key,
            'is_valid': InvitationKey.objects.is_key_valid(invitation_key),
        })
        return context
