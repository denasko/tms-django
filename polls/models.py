from django.db import models
from django.db.models import QuerySet, CharField
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', db_index=True)
    publication = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    objects: QuerySet

    def was_published_recently(self) -> int:
        now = timezone.now()
        return now - timezone.timedelta(days=1) <= self.pub_date <= now

    def __str__(self) -> CharField:
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    objects: QuerySet

    def __str__(self) -> str:
        return f'{self.question.question_text} - {self.choice_text}'
