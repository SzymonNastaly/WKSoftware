from django.contrib import admin

from .models import Competition, Run, Relay


admin.site.register(Competition)
admin.site.register(Run)
admin.site.register(Relay)
