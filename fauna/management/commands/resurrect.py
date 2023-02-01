from django.core.management.base import BaseCommand

from fauna.models import Animal


class Command(BaseCommand):
    help = "Kathulu sleeps under the see"

    def add_arguments(self, parser):
        parser.add_argument("-c", "--color", help="Add some color to life", default="green")
        parser.add_argument("-m", "--meister", action="store_true", default=False)
        parser.add_argument("--ids", nargs="+", type=int)

    def handle(self, *args, **kwargs):
        extinct_animals = Animal.objects.all()
        for animal in extinct_animals:
            self.stdout.write(f"He has awaken {animal.name} in order to {kwargs.get('wish')} and might paint him in {kwargs.get('color')}")
            if kwargs.get("meister"):
                self.stdout.write(f"going to resurrect {animal.name}")
                animal.its_alive = True
                animal.save()

        for an_id in kwargs.get("ids"):
            self.stdout.write(f"{an_id}")

