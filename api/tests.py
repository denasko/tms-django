from django.test import TestCase
from django.utils import timezone

from articles.models import Article, Author
from polls.models import Question, Choice


class BaseAPITestCase(TestCase):
    def assertEmptyResponse(self, path: str):
        response = self.client.get(path)
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['count'], 0)
        self.assertEqual(data['results'], [])

    def assertReturnJson(self, path: str, model: Question | Choice | Article):
        if model == Question or model == Choice:

            question1 = Question.objects.create(question_text='Hello', pub_date=timezone.now())
            question2 = Question.objects.create(question_text='Its me', pub_date=timezone.now())
            Choice.objects.create(question=question1, choice_text='Privet')
            Choice.objects.create(question=question2, choice_text='Always me')

        elif model == Article:

            author1 = Author.objects.create(name='Den')
            author2 = Author.objects.create(name='Petya')
            Article.objects.create(title='Jinja', content='Jinja - top', pub_date=timezone.now(), author=author1)
            Article.objects.create(title='I and zavod', content='Love', pub_date=timezone.now(), author=author2)

        response = self.client.get(path)
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data['count'], 2)

    def assertNotReally(self, path: str):
        response = self.client.get(path)
        self.assertEquals(response.status_code, 404)


# ___________________________________________Pols________________________________________
class QuestionsAPITest(BaseAPITestCase):
    def test_empty_questions(self):
        self.assertEmptyResponse('/api/questions/')

    def test_return_json_questions(self):
        self.assertReturnJson(path='/api/questions/', model=Question)

    def test_not_really_question(self):
        self.assertNotReally('/api/questions/1/')

    def test_return_detail_questions(self):
        question0 = Question.objects.create(question_text='Hello', pub_date=timezone.now())
        question1 = Question.objects.create(question_text='Its me', pub_date=timezone.now())
        Choice.objects.create(question=question0, choice_text='Privet')
        Choice.objects.create(question=question1, choice_text='Always me')

        response = self.client.get('/api/questions/')
        data = response.json()

        self.assertEqual(data['results'][0]['question_text'], 'Hello')
        self.assertEqual(data['results'][1]['question_text'], 'Its me')
        self.assertEqual(data['results'][0]['choices'][0]['choice_text'], 'Privet')
        self.assertEqual(data['results'][1]['choices'][0]['choice_text'], 'Always me')


class ChoicesAPITest(BaseAPITestCase):
    def test_empty_choices(self):
        self.assertEmptyResponse('/api/choices/')

    def test_return_json_choices(self):
        self.assertReturnJson(path='/api/choices/', model=Choice)

    def test_not_really_choices(self):
        self.assertNotReally('/api/choices/1/')

    def test_return_detail_choice(self):
        question0 = Question.objects.create(question_text='Hello', pub_date=timezone.now())
        question1 = Question.objects.create(question_text='Its me', pub_date=timezone.now())
        Choice.objects.create(question=question0, choice_text='Privet')
        Choice.objects.create(question=question1, choice_text='Always me')

        response = self.client.get('/api/choices/')
        data = response.json()

        self.assertEqual(data['results'][0]['question'], 1)  # Question.pk
        self.assertEqual(data['results'][1]['question'], 2)  # Question.pk
        self.assertEqual(data['results'][0]['choice_text'], 'Privet')
        self.assertEqual(data['results'][1]['choice_text'], 'Always me')


# _____________________________________________Articles____________________________________
class ArticlesAPITest(BaseAPITestCase):

    def test_empty_articles(self):
        self.assertEmptyResponse('/api/articles/')

    def test_return_json_articles(self):
        self.assertReturnJson(path='/api/articles/', model=Article)

    def test_not_really_article(self):
        self.assertNotReally('/api/article/1/')

    def test_return_detail_articles(self):
        author1 = Author.objects.create(name='Den')
        author2 = Author.objects.create(name='Petya')
        Article.objects.create(title='Jinja', content='Jinja - top', pub_date=timezone.now(), author=author1)
        Article.objects.create(title='I and zavod', content='Love', pub_date=timezone.now(), author=author2)

        response = self.client.get('/api/articles/')
        data = response.json()

        self.assertEqual(data['results'][0]['author'], 1)  # Question.pk
        self.assertEqual(data['results'][1]['author'], 2)  # Question.pk
        self.assertEqual(data['results'][0]['title'], 'Jinja')
        self.assertEqual(data['results'][1]['title'], 'I and zavod')
        self.assertEqual(data['results'][0]['content'], 'Jinja - top')
        self.assertEqual(data['results'][1]['content'], 'Love')

# _______________________________________Shop___________________________________________
