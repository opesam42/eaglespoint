from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
    help = "Displays current time"

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help="Indicate total")

    def handle(self, *args, **kwargs):
        total = kwargs["total"]
        for i in range(total):
            self.stdout.write("Hello, testing command!")