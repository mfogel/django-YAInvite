from django.contrib import admin
from .models import Invite

class InviteAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'invitor', 'invited', 'is_expired', 'is_redeemed')

admin.site.register(Invite, InviteAdmin)
