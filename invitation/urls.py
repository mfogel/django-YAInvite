from django.conf.urls.defaults import patterns, url

from invitation.views import (
        SendInviteView, InviteSentView,
        RedeemInviteView, InviteRedeemedView)


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
    url(r'^redeemed/(?P<invitation_key>\w+)/$',
        InviteRedeemedView.as_view(),
        name='invitation_redeemed'
    ),
)
