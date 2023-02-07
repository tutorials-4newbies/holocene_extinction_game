from django.core.management import BaseCommand

from fauna.models import Animal


class Command(BaseCommand):
    help = "Kathulu sleeps under the sea"

    def add_arguments(self, parser):
        parser.add_argument("-g", "--god_mode", action="store_true", default=False, help="This is god mode for dangerous stuff")
        parser.add_argument("--users", type=int, nargs="*")

    def handle(self, *args, **options):
        self.stdout.write("The dead would rise")
        if options.get("god_mode"):
            self.stdout.write("Do something dangerous")
            dead_animals = Animal.objects.filter(its_alive=False)

            dead_animals.update(its_alive=True)

