from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from rasacore.training import Train

class Command(BaseCommand):
    help = 'Training base on core.rasa.ai'

    def handle(self, *args, **options):
        try:
            train_cls = Train()
            train_cls.run()
        except Exception as ex:
            raise CommandError('Error %s ' % str(ex))

        self.stdout.write(self.style.SUCCESS('Done training models'))