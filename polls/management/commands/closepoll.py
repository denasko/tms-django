from django.core.management.base import BaseCommand, CommandError

from polls.models import Question as Poll


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        for poll_id in options['poll_ids']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError(f'Poll {poll_id} does not exists')

            poll.opened = False
            poll.save()

            self.stdout.write(
                self.style.SUCCESS(f'Successfully closed poll {poll_id}')
            )
