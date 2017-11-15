# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Intents, Actions, Stories, \
    IntentEntities, IntentUserSays

class IntentUserSaysInline(admin.StackedInline):
    model = IntentUserSays

class IntentEntitiesInline(admin.StackedInline):
    model = IntentEntities

class IntentsAdmin(admin.ModelAdmin):
    inlines = [IntentEntitiesInline, IntentUserSaysInline, ]

admin.site.register(Intents, IntentsAdmin)
admin.site.register(Actions)
admin.site.register(Stories, DraggableMPTTAdmin)
