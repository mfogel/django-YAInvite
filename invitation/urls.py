from django.conf.urls.defaults import *

from invitation.views import SendInviteView, InviteSentView, RedeemInviteView

urlpatterns = patterns('',
    url(r'^send/$',
        SendInviteView.as_view(),
        name='invitation_send'
    ),
    url(r'^sent/$',
        InviteSentView.as_view(),
        name='invitation_sent'
    ),
    url(r'^redeem/(?P<invitation_key>\w+)/$',
        RedeemInviteView.as_view(),
        name='invitation_redeem'
    ),
)
