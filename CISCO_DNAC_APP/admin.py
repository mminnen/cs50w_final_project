from django.contrib import admin

from CISCO_DNAC_APP.models import DnacControllers, WebhookEvents

# Register your models here.
admin.site.register(DnacControllers)
admin.site.register(WebhookEvents)

