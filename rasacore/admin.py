# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from solo.admin import SingletonModelAdmin
from mptt.admin import DraggableMPTTAdmin

from .models import Intents, Actions, Stories, \
    IntentEntities, IntentUserSays, Training, \
    StoryActions, StoryActionsResponses

class IntentUserSaysInline(admin.StackedInline):
    model = IntentUserSays

class IntentEntitiesInline(admin.StackedInline):
    model = IntentEntities

class StoryActionsInline(admin.StackedInline):
    model = StoryActions

class IntentsAdmin(admin.ModelAdmin):
    inlines = [IntentEntitiesInline, IntentUserSaysInline, ]

class StoriesAdmin(DraggableMPTTAdmin):
    inlines = [StoryActionsInline, ]
    
admin.site.register(Intents, IntentsAdmin)
admin.site.register(Actions)
admin.site.register(StoryActionsResponses)
admin.site.register(Stories, StoriesAdmin)
admin.site.register(Training, SingletonModelAdmin)
