from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Kathulu sleeps under the see"

    def handle(self, *args, **options):
        self.stdout.write("He has awaken")
