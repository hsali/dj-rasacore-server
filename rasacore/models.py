# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from solo.models import SingletonModel
from django.db.models.signals import post_save

class Actions(models.Model):
    name = models.SlugField(max_length=70)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'

class Entities(models.Model):
    name = models.SlugField(max_length=70)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Entity'
        verbose_name_plural = 'Entities'

class Intents(models.Model):
    name = models.SlugField(max_length=70)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Intent'
        verbose_name_plural = 'Intents'

class IntentUserSays(models.Model):
    """
    NLU user says examples. Examples of conversation texts users have with the bot
    """
    intent = models.ForeignKey(Intents, related_name='usersays')
    text = models.CharField(max_length=240)

    class Meta:
        verbose_name = 'Intent User Say'
        verbose_name_plural = 'Intent User Says'

class IntentUserSaysEntities(models.Model):
    usersay = models.ForeignKey(IntentUserSays, related_name='entities')
    entity = models.ForeignKey(Entities, related_name='intent_entities')
    value = models.CharField(max_length=140)
    # TODO: Change synonyms field to Postgres array field
    synonyms = models.CharField(max_length=400, blank=True, null=True, help_text="Add multiple value synonyms separated by commas")
    start = models.IntegerField(default=0, editable=False)
    end = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name = 'User Says Entity'
        verbose_name_plural = 'User Says Entities'

class Stories(MPTTModel):
    title = models.CharField(max_length=70)
    intent = models.ForeignKey(Intents, related_name='stories')

    # Link stories together to create a path
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    def __unicode__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'

class StoryActions(models.Model):
    story = models.ForeignKey(Stories, related_name='actions')
    action = models.ForeignKey(Actions, related_name='story_actions')

    def __unicode__(self):
        return "%s (%s)" % (self.action, self.story)

class StoryActionsResponses(models.Model):
    story_action = models.ForeignKey(StoryActions, related_name='responses')
    text = models.CharField(max_length=240)

    def __unicode__(self):
        return '%s response' % self.story_action

    class Meta:
        verbose_name = 'Action response'
        verbose_name_plural = 'Action responses'

class ResponseButtons(models.Model):
    response = models.ForeignKey(StoryActionsResponses, related_name='buttons')
    title =  models.CharField(max_length=20)
    payload =  models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Button'
        verbose_name_plural = 'Buttons'

class Training(SingletonModel):
    PIPELINE_CHOICES = (
        ('spacy_sklearn', 'Spacy-Sklearn'), 
    )
    pipeline = models.CharField(max_length=70, choices=PIPELINE_CHOICES, default='spacy_sklearn')

    def __unicode__(self):
        return u"Training"

    class Meta:
        verbose_name = "Training"


def on_user_entities_save(sender, instance, created, **kwargs):
    try:
        if instance.value and instance.usersay.text:
            example_text = instance.usersay.text
            start = example_text.find(instance.value)
            end = len(instance.value) + start
            if (instance.start != start) and (instance.end != end):
                instance.start = start
                instance.end = end
                instance.save()
    except Exception as ex:
        print(str(ex))
post_save.connect(on_user_entities_save, sender=IntentUserSaysEntities)