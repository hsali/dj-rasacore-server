import yaml
import os
from django.conf import settings

class Train:

    def build_domain(self):
        """
        Create domains dict
        """
        return {
            'intents': ['greet', 'goodbye'],
            'templates': [
                {
                    'utter_greet': {
                        'text': 'How are you',
                        'buttons': [
                            {'title': 'great', 'payload': 'great'},
                            {'title': 'sad', 'payload': 'sad'}
                        ]
                    },
                    'utter_cheerup': {
                        'text': 'How are you',
                        'buttons': [
                            {'title': 'great', 'payload': 'great'},
                            {'title': 'sad', 'payload': 'sad'}
                        ]
                    }
                }
            ],
            'actions': ['utter_greet', 'utter_cheer_up']
        }
    def compose_files(self):
        """
        Collect data from django models and create training files as 
        expected by core.rasa.ia commands
        
        Outputs: 
            nlu_model_config.json
            domains.yml
            data/nlu.md
            data/stories.md
        """
        domain = self.build_domain()
        domain_file = os.path.join(settings.TRAINING_DIR, 'domain.yml')
        with open(domain_file, 'w') as outfile:
            yaml.dump(domain, outfile, default_flow_style=False)