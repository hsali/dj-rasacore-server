from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core.domain import TemplateDomain
from rasa_core.training_utils.dsl import StoryFileReader
from rasa_core.training_utils.visualization import visualize_stories

if __name__ == '__main__':
    domain = TemplateDomain.load("trainingdump/domain.yml")
    stories = StoryFileReader.read_from_file("trainingdump/story.md", domain)

    visualize_stories(stories, "trainingdump/graph.png")