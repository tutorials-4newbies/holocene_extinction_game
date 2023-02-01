from django.core.management.base import BaseCommand

from fauna.models import Animal


class Command(BaseCommand):
    help = "Kathulu sleeps under the see"

    def add_arguments(self, parser):
        #  POSITIONAL argument
        parser.add_argument("wish", help="what he would wish to do", type=str)
        parser.add_argument("-c", "--color", help="Add some color to life", default="green")

    def handle(self, *args, **kwargs):
        extinct_animals = Animal.objects.all()
        for animal in extinct_animals:
            self.stdout.write(f"He has awaken {animal.name} in order to {kwargs.get('wish')} and might paint him in {kwargs.get('color')}")
