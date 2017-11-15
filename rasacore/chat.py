import os
from django.conf import settings
from rasa_core.agent import Agent

class Chat:
    """
    Clone https://github.com/RasaHQ/rasa_core/blob/master/rasa_core/server.py
    """
    TRAINING_DIR = settings.TRAINING_DIR

    def __init__(self):
        dialogue = os.path.join(self.TRAINING_DIR, 'dialogue')
        interpreter = os.path.join(self.TRAINING_DIR, 'models/default')
        self.agent = Agent.load(dialogue, interpreter=interpreter)

    def handle_message(self, message):
        return self.agent.handle_message(message)

# chat.agent.start_message_handling