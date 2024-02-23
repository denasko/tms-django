import json

from django.core.management.base import BaseCommand
from django.utils import timezone

from polls.models import Question, Choice


class Command(BaseCommand):
    help = 'Populate the polls database with initial data'

    def add_arguments(self, parser):
        parser.add_argument('data_file_path', nargs='+', type=str)

    def handle(self, *args, **options):
        if options:
            path = ''.join(options['data_file_path'])
        else:
            path = 'initial_data_polls.json'

        with open(path, 'r') as file:
            data = json.load(file)

        for question_text, choices_data in data.items():
            question = Question.objects.create(
                question_text=question_text,
                pub_date=timezone.now(),
                publication=True
            )

            for choice_text, votes in choices_data.items():
                Choice.objects.create(
                    question=question,
                    choice_text=choice_text,
                    votes=votes
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the polls database'))
