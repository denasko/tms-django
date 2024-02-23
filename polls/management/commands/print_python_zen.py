from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Prints python zen'

    def handle(self, *args, **options):
        import this
