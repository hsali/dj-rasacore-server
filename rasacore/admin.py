# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from solo.admin import SingletonModelAdmin
from mptt.admin import DraggableMPTTAdmin

from .models import Intents, Actions, Stories, \
    IntentUserSaysEntities, IntentUserSays, Training, \
    StoryActions, StoryActionsResponses, ResponseButtons, \
    Entities

class IntentUserSaysInline(admin.StackedInline):
    model = IntentUserSays

class IntentUserSaysEntitiesInline(admin.StackedInline):
    model = IntentUserSaysEntities
    readonly_fields = ['start', 'end']

class StoryActionsInline(admin.StackedInline):
    model = StoryActions

class IntentsAdmin(admin.ModelAdmin):
    inlines = [IntentUserSaysInline, ]

class StoriesAdmin(DraggableMPTTAdmin):
    inlines = [StoryActionsInline, ]

class IntentUserSaysAdmin(admin.ModelAdmin):
    list_display = ['intent', 'text']
    list_filter = ['intent', ]
    search_fields = ['text', ]
    inlines = [IntentUserSaysEntitiesInline, ]

class ResponseButtonsInline(admin.TabularInline):
    model = ResponseButtons

class EntitiesAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]

class StoryActionsResponsesAdmin(admin.ModelAdmin):
    inlines = [ResponseButtonsInline, ]
    list_filter = ['story_action', ]
    search_fields = ['text', ]
    
admin.site.register(Intents, IntentsAdmin)
admin.site.register(Actions)
admin.site.register(StoryActionsResponses, StoryActionsResponsesAdmin)
admin.site.register(IntentUserSays, IntentUserSaysAdmin)
admin.site.register(Stories, StoriesAdmin)
admin.site.register(Entities, EntitiesAdmin)
admin.site.register(Training, SingletonModelAdmin)
