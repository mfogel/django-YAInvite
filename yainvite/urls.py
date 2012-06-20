from django.conf.urls.defaults import patterns, url

from .views import (
        SendInviteView, InviteSentView,
        RedeemInviteView, InviteRedeemedView)


urlpatterns = patterns('',
    url(r'^send/$',
        SendInviteView.as_view(),
        name='yainvite_send'
    ),
    url(r'^sent/$',
        InviteSentView.as_view(),
        name='yainvite_sent'
    ),
    url(r'^redeem(?:/(?P<invite_key>\w+))?/$',
        RedeemInviteView.as_view(),
        name='yainvite_redeem'
    ),
    url(r'^redeemed/$',
        InviteRedeemedView.as_view(),
        name='yainvite_redeemed'
    ),
)
