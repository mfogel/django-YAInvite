from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from .backends import get_backend
from .models import Invite
from .forms import SendInviteForm


class LoginRequiredMixin(object):
    "Restrict a View to only logged-in Users"
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class SendInviteView(LoginRequiredMixin, FormView):
    "Send an invite"
    form_class = SendInviteForm
    template_name = 'yainvite/send.html'
    success_url = reverse_lazy('yainvite_sent')

    def dispatch(self, request, *args, **kwargs):
        self.invite_backend = get_backend(request=request)
        return super(SendInviteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SendInviteView, self).get_context_data(**kwargs)
        context['number_invites_remaining'] = (
                self.invite_backend.number_invites_remaining)
        return context

    def form_valid(self, form):
        "Send the invite"
        invite = Invite.objects.create_invite(self.invite_backend.inviter)
        self.invite_backend.number_invites_remaining -= 1
        invite.send_to(form.cleaned_data['email'])
        return super(SendInviteView, self).form_valid(form)


class InviteSentView(LoginRequiredMixin, TemplateView):
    "Invite successfully sent - success page"
    template_name = 'yainvite/sent.html'


class RedeemInviteView(FormView):
    "Redeem an invite"
    form_class = UserCreationForm
    template_name = 'yainvite/redeem.html'
    success_url = reverse_lazy('yainvite_redeemed')

    def dispatch(self, request, *args, **kwargs):
        self.invite_key = kwargs.get('invite_key')
        self.invite = Invite.objects.get_invite(self.invite_key)
        return super(RedeemInviteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RedeemInviteView, self).get_context_data(**kwargs)
        context.update({
            'invite_key': self.invite_key,
            'invite': self.invite,
        })
        return context

    def form_valid(self, form):
        "Redeem the invite"
        if not self.invite:
            return super(RedeemInviteView, self).form_invalid(form)
        new_user = form.save()
        self.invite.redeem(new_user)
        return super(RedeemInviteView, self).form_valid(form)


class InviteRedeemedView(TemplateView):
    "Invite successfully redeemed - success page"
    template_name = 'yainvite/redeemed.html'
