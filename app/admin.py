from django.contrib import admin
from .models import IntegrationSettings, Integrations

admin.site.register(IntegrationSettings)
admin.site.register(Integrations)
