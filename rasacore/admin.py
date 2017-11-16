# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import nested_admin
from django.contrib import admin
from solo.admin import SingletonModelAdmin
from mptt.admin import DraggableMPTTAdmin

from .models import Intents, Actions, Stories, \
    IntentUserSaysEntities, IntentUserSays, Training, \
    StoryActions, StoryActionsResponses, ResponseButtons, \
    Entities

# Intent based admins
class IntentUserSaysEntitiesInline(nested_admin.NestedTabularInline):
    model = IntentUserSaysEntities
    readonly_fields = ['start', 'end']
    extra = 0
    classes = ['collapse']

class IntentUserSaysInline(nested_admin.NestedStackedInline):
    model = IntentUserSays
    inlines = [IntentUserSaysEntitiesInline, ]
    extra = 0
    classes = ['collapse']

class IntentsAdmin(nested_admin.NestedModelAdmin):
    inlines = [IntentUserSaysInline, ]

# Stories admin
class ResponseButtonsInline(nested_admin.NestedTabularInline):
    model = ResponseButtons
    extra = 0
    classes = ['collapse']

class StoryActionsResponsesInline(nested_admin.NestedStackedInline):
    model = StoryActionsResponses
    inlines = [ResponseButtonsInline, ]
    extra = 0
    classes = ['collapse']

class StoryActionsInline(nested_admin.NestedStackedInline):
    model = StoryActions
    inlines = [StoryActionsResponsesInline, ]
    extra = 0
    classes = ['collapse']

class StoriesAdmin(nested_admin.NestedModelAdmin, DraggableMPTTAdmin):
    inlines = [StoryActionsInline, ]

class EntitiesAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]

admin.site.register(Intents, IntentsAdmin)
admin.site.register(Actions)
admin.site.register(Stories, StoriesAdmin)
admin.site.register(Entities, EntitiesAdmin)
admin.site.register(Training, SingletonModelAdmin)
