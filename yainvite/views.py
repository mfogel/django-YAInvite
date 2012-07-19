from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from extra_views.multi import MultiFormView

from .backends import get_backend
from .forms import SendInviteForm, RedeemInviteForm
from .utils import import_class


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
        if self.invite_backend.number_invites_remaining > 0:
            self.invite_backend.number_invites_remaining -= 1
            form.send(self.invite_backend.inviter,
                    domain=self.request.META['HTTP_HOST'])
        return super(SendInviteView, self).form_valid(form)


class InviteSentView(LoginRequiredMixin, TemplateView):
    "Invite successfully sent - success page"
    template_name = 'yainvite/sent.html'


class RedeemInviteView(MultiFormView):
    "Redeem an invite"

    forms = {
        'user': MultiFormView.form(
            import_class(settings.YAINVITE_USER_CREATION_FORM)
        ),
        'invite': MultiFormView.form(RedeemInviteForm),
    }
    template_name = 'yainvite/redeem.html'
    success_url = reverse_lazy(settings.YAINVITE_REDIRECT_NEW_USER_TO)

    def get_initial_invite(self):
        return {'key': self.kwargs.get('invite_key', '')}

    def valid_all(self, forms):
        "Redeem the invite"
        new_user = forms['user'].save_and_authenticate()
        forms['invite'].redeem(new_user)
        login(self.request, new_user)


class InviteRedeemedView(TemplateView):
    "Invite successfully redeemed - success page"
    template_name = 'yainvite/redeemed.html'
