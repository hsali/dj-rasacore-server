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

from .models import Intents, IntentActions, IntentUserSays, \
    Stories, IntentActionsResponses, IntentUserSaysEntities, \
    Entities

class Train:
    TRAINING_DIR = settings.TRAINING_DIR

    def split_synonyms(self, synonyms):
        """
        Split comma separated synonyms and return an array
        """
        try:
            if synonyms:
                return synonyms.split(',')
            return []
        except Exception as ex:
            print(ex)
            return []

    def get_training_data(self):
        # Compose training data from models
        common_examples = []
        entity_synonyms = []
        user_says = IntentUserSays.objects.all()
        for user_say in user_says:
            entities = [{ 'start': int(entity.start), 'end': int(entity.end), 'value': str(entity.value), 'entity': str(entity.entity.name) }\
                 for entity in user_say.entities.all()]
            common_examples.append({
                'text': user_say.text,
                'intent': user_say.intent.name,
                'entities': entities
            })

        user_say_entities = IntentUserSaysEntities.objects.all()
        entity_synonyms = [{'value': entity.value, 'synonyms': self.split_synonyms(entity.synonyms)} for entity in user_say_entities]

        # Put everything together
        rasa_nlu_data = {
            'rasa_nlu_data': {
                'common_examples': common_examples,
                'entity_synonyms': entity_synonyms
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
            'pipeline': [
                'nlp_spacy', 
                'tokenizer_spacy', 
                'intent_entity_featurizer_regex', 
                'intent_featurizer_spacy', 
                'ner_crf', 
                'ner_synonyms', 
                'intent_classifier_sklearn', 
                'ner_duckling'
            ]
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
        responses = IntentActionsResponses.objects.all()
        for response in responses:
            response_temp = dict()
            action_name = str(response.intent_action.action.name)
            buttons = [{'title': str(button.title), 'payload': str(button.payload)} for button in response.buttons.all()]
            response_temp[action_name] = [{'text': str(response.text), 'buttons':buttons}]
            templates.update(response_temp)

        # Compose slots
        entities = Entities.objects.all()
        slots = {}
        for entity in entities:
            slots[str(entity.name)] = {'type': 'text'}

        # Put everything together
        domain_data = {
            "intents": list(set([str(intent.name) for intent in Intents.objects.all()])),
            "actions": list(set([str(intent_action.action.name) for intent_action in IntentActions.objects.all()])),
            "templates": templates,
            "entities": list(set([str(entity.name) for entity in entities])),
            "slots": slots
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
            # Add intent and actions
            for intent in story.intents.all():
                story_string += '* _%s\n' % intent.name
                for action_item in intent.actions.all():
                    story_string += '\t- %s\n' % action_item.action.name
            
            # Break with new line to separate with new story
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
        