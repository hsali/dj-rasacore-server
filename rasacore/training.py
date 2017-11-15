import yaml
import os
import json
from django.conf import settings

from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.agent import Agent
from rasa_core.domain import TemplateDomain, Domain

from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer

from .models import Intents, StoryActions, IntentUserSays, \
    Stories, StoryActionsResponses

class Train:
    TRAINING_DIR = settings.TRAINING_DIR

    def get_training_data(self):
        # Compose training data from models
        common_examples = []
        user_says = IntentUserSays.objects.all()
        for user_say in user_says:
            common_examples.append({
                'text': user_say.text,
                'intent': user_say.intent.name,
                'entities': []
            })

        rasa_nlu_data = {
            'rasa_nlu_data': {
                'common_examples': common_examples
            }
        }

        # Write result to file
        training_file = os.path.join(self.TRAINING_DIR, 'rasa_nlu_data.json')
        with open(training_file, 'w') as outfile:
            outfile.write(json.dumps(rasa_nlu_data))
        
        training_data = load_data(training_file)
        return training_data

    def get_config_file(self):
        """
        Open and write configuration to the provided file
        """
        configuration = {
            'pipeline': 'spacy_sklearn'
        }
        config_file = os.path.join(self.TRAINING_DIR, 'config_spacy.json')
        with open(config_file, 'w') as outfile:
            outfile.write(json.dumps(configuration))
        return config_file

    def nlu_train_models(self):
        training_data = self.get_training_data()
        
        trainer = Trainer(RasaNLUConfig(self.get_config_file()))
        trainer.train(training_data)
        model_directory = trainer.persist(os.path.join(self.TRAINING_DIR, 'models')) 

    def compose_domain_file(self):
        """
        Generate domain.yml file
        
        See:
        Example of expected json output of a valid generated yalm file https://jsonformatter.org/b9c066
        """
        templates = {}
        responses = StoryActionsResponses.objects.all()
        for response in responses:
            response_temp = dict()
            action_name = str(response.story_action.action.name)
            response_temp[action_name] = [{'text': str(response.text), 'buttons':[]}]
            templates.update(response_temp)

        domain_data = {
            "intents": [str(intent.name) for intent in Intents.objects.all()],
            "actions": [str(story_action.action.name) for story_action in StoryActions.objects.all()],
            "templates": templates
        }

        domain_file = os.path.join(self.TRAINING_DIR, 'domain.yml')
        with open(domain_file, 'w') as outfile:
            yaml.dump(domain_data, outfile, default_flow_style=False)
        return domain_file

    def compose_story_file(self):
        """
        Generate the story.md file
        """
        stories = Stories.objects.all()

        story_string = ''
        for story in stories:
            story_string += '## %s\n' % story.title
            story_string += '*_%s\n' % story.intent.name
            for action_item in story.actions.all():
                story_string += '-%s\n' % action_item.action.name
            story_string += '\n'
        
        story_file = os.path.join(self.TRAINING_DIR, 'story.md')
        with open(story_file, 'w') as outfile:
            outfile.write(story_string)
        return story_file

    def train_dialogue(self):
        domain_file = os.path.join(self.TRAINING_DIR, 'domain.yml')
        stories_file = os.path.abspath(os.path.join(self.TRAINING_DIR, 'story.md'))

        domain = TemplateDomain.load(domain_file)
        # domain.compare_with_specification(os.path.join(self.TRAINING_DIR, 'dialogue'))
        agent = Agent(domain, policies=[MemoizationPolicy(), KerasPolicy()])
        agent.train(stories_file,validation_split=0.1)
        agent.persist(os.path.join(self.TRAINING_DIR, 'dialogue'))

    def run(self):
        # NLU training
        self.nlu_train_models()

        # Dialog training
        self.compose_domain_file()
        self.compose_story_file()
        self.train_dialogue()

    # def build_domain(self):
    #     """
    #     Create domains dict
    #     """
    #     return {
    #         'intents': ['greet', 'goodbye'],
    #         'templates': [
    #             {
    #                 'utter_greet': {
    #                     'text': 'How are you',
    #                     'buttons': [
    #                         {'title': 'great', 'payload': 'great'},
    #                         {'title': 'sad', 'payload': 'sad'}
    #                     ]
    #                 },
    #                 'utter_cheerup': {
    #                     'text': 'How are you',
    #                     'buttons': [
    #                         {'title': 'great', 'payload': 'great'},
    #                         {'title': 'sad', 'payload': 'sad'}
    #                     ]
    #                 }
    #             }
    #         ],
    #         'actions': ['utter_greet', 'utter_cheer_up']
    #     }
    
    # def build_story(self):
    #     return {
    #         '##happy path': {"_greet": ["utter_greet"], "_mood_great": ["utter_happy", "utter_greet"]}
    #     }
        
    # def compose_files(self):
    #     """
    #     Collect data from django models and create training files as 
    #     expected by core.rasa.ia commands
        
    #     Outputs: 
    #         nlu_model_config.json
    #         domains.yml
    #         data/nlu.md
    #         data/stories.md
    #     """
    #     domain = self.build_domain()
    #     domain_file = os.path.join(settings.TRAINING_DIR, 'domain.yml')
    #     with open(domain_file, 'w') as outfile:
    #         yaml.dump(domain, outfile, default_flow_style=False)

    #     story = self.build_story()
    #     story_file = os.path.join(settings.TRAINING_DIR, 'story.md')
    #     with open(story_file, 'w') as outfile:
    #         yaml.dump(story, outfile, default_flow_style=False)