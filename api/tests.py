from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from polls.models import Question


class QuestionViewTest(TestCase):

    def test_empty_db(self):
        response = self.client.get('/api/questions/')
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data, [])

    def test_with_question(self):
        Question.objects.create(question_text='Hello', pub_date=timezone.now())
        Question.objects.create(question_text='Its me', pub_date=timezone.now())

        response = self.client.get('/api/questions/')
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(len(data), 2)
        self.assertEquals(data[0]['question_text'], 'Hello')
        self.assertEquals(data[1]['question_text'], 'Its me')

    def test_not_really_question(self):
        response = self.client.get(reverse('polls:detail', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, 404)

    def test_return_json(self):
        question = Question.objects.create(question_text='Hello', pub_date=timezone.now())

        response = self.client.get(reverse('polls:detail', kwargs={'pk': question.pk}))
        self.assertEquals(response.status_code, 200)

        self.assertEquals(question.question_text, question.question_text)
