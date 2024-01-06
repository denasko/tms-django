import json

from django.utils import timezone

from polls.models import Question, Choice


def populate_polls_database(path: str, clean_database: bool = False):
    with open(path, 'r') as file:
        data = json.load(file)

        if clean_database:
            Question.objects.all().delete()

    for question_text, choices in data.items():
        question = Question.objects.create(question_text=question_text, pub_date=timezone.now())

        for choice_text, votes in choices.items():
            Choice.objects.create(question=question, choice_text=choice_text, votes=votes)


