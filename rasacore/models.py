# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Actions(models.Model):
    name = models.CharField(max_length=70)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'

class Entities(models.Model):
    name = models.CharField(max_length=70)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Entity'
        verbose_name_plural = 'Entities'

class Intents(models.Model):
    name = models.CharField(max_length=70)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Intent'
        verbose_name_plural = 'Intents'

class IntentEntities(models.Model):
    intent = models.ForeignKey(Intents, related_name='entities')
    entity = models.ForeignKey(Entities, related_name='intent_entities')
    value = models.CharField(max_length=140)

    class Meta:
        verbose_name = 'Intent Entity'
        verbose_name_plural = 'Intent Entities'

class IntentUserSays(models.Model):
    """
    NLU user says examples. Examples of conversation texts users have with the bot
    """
    intent = models.ForeignKey(Intents, related_name='usersays')
    text = models.CharField(max_length=240)

    class Meta:
        verbose_name = 'Intent User Say'
        verbose_name_plural = 'Intent User Says'

class Stories(MPTTModel):
    title = models.CharField(max_length=70)
    intent = models.ForeignKey(Intents, related_name='stories')
    actions = models.ForeignKey(Actions, related_name='stories')

    # Link stories together to create a path
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    def __unicode__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'
