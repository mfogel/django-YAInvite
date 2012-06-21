from django.contrib import admin
from .models import Invite, EmailEvent

class InviteAdmin(admin.ModelAdmin):
    list_display = (
            '__unicode__', 'inviter', 'invited', 'is_expired', 'is_redeemed')

class EmailEventAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'invite', 'sent_to', 'sent_at')


admin.site.register(Invite, InviteAdmin)
admin.site.register(EmailEvent, EmailEventAdmin)
