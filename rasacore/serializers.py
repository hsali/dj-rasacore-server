from rest_framework import serializers

from .models import Actions, Entities, Intents, \
    IntentUserSays, IntentUserSaysEntities, Stories, \
    IntentActions, IntentActionsResponses, ResponseButtons, Training


class ActionsSer(serializers.ModelSerializer):
    class Meta:
        model = Actions
        fields = "__all__"

class EntitiesSer(serializers.ModelSerializer):
    class Meta:
        model = Entities
        fields = "__all__"

class IntentsSer(serializers.ModelSerializer):
    class Meta:
        model = Intents
        fields = "__all__"

class IntentUserSaysSer(serializers.ModelSerializer):
    class Meta:
        model = IntentUserSays
        fields = "__all__"

class IntentUserSaysEntitiesSer(serializers.ModelSerializer):
    class Meta:
        model = IntentUserSaysEntities
        fields = "__all__"

class StoriesSer(serializers.ModelSerializer):
    class Meta:
        model = Stories
        fields = "__all__"

class IntentActionsSer(serializers.ModelSerializer):
    class Meta:
        model = IntentActions
        fields = "__all__"

class IntentActionsResponsesSer(serializers.ModelSerializer):
    class Meta:
        model = IntentActionsResponses
        fields = "__all__"

class ResponseButtonsSer(serializers.ModelSerializer):
    class Meta:
        model = ResponseButtons
        fields = "__all__"


class TrainingSer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = "__all__"