# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import nested_admin
from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import Intents, Actions, Stories, \
    IntentUserSaysEntities, IntentUserSays, Training, \
    IntentActions, IntentActionsResponses, ResponseButtons, \
    Entities

# Intent based admins
class IntentUserSaysEntitiesInline(nested_admin.NestedTabularInline):
    model = IntentUserSaysEntities
    readonly_fields = ['start', 'end']
    extra = 1

class IntentUserSaysInline(nested_admin.NestedStackedInline):
    model = IntentUserSays
    inlines = [IntentUserSaysEntitiesInline, ]
    extra = 1

class IntentsAdmin(nested_admin.NestedModelAdmin):
    inlines = [IntentUserSaysInline, ]

# Stories admin
class ResponseButtonsInline(nested_admin.NestedTabularInline):
    model = ResponseButtons
    extra = 1

class IntentActionsResponsesInline(nested_admin.NestedStackedInline):
    model = IntentActionsResponses
    inlines = [ResponseButtonsInline, ]
    extra = 1

class IntentActionsInline(nested_admin.NestedStackedInline):
    model = IntentActions
    inlines = [IntentActionsResponsesInline, ]
    extra = 1

class IntentsInline(nested_admin.NestedStackedInline):
    model = Intents
    inlines = [IntentActionsInline, ]

class StoriesAdmin(nested_admin.NestedModelAdmin):
    inlines = [IntentsInline, ]

class EntitiesAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]

admin.site.register(Intents, IntentsAdmin)
admin.site.register(Actions)
admin.site.register(Stories, StoriesAdmin)
admin.site.register(Entities, EntitiesAdmin)
admin.site.register(Training, SingletonModelAdmin)
