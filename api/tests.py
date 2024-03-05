from django.test import TestCase
from django.utils import timezone

from articles.models import Article, Author
from polls.models import Question, Choice
from shop.models import Product, Category


class BaseAPITestCase(TestCase):

    def get_response_with_db(self, path: str, model: Question | Choice | Article):
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

        elif model == Product or model == Category:
            category1 = Category.objects.create(category_name='phones')
            category2 = Category.objects.create(category_name='notebooks')

            Product.objects.create(product_name='Iphone', description='top', price=100, category=category1,
                                   is_published=True, pub_date=timezone.now())

            Product.objects.create(product_name='Asus', description='for gaming', price=110, category=category2,
                                   is_published=True, pub_date=timezone.now())

        response = self.client.get(path)
        return response

    def assertEmptyResponse(self, path: str):
        response = self.client.get(path=path)
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['count'], 0)
        self.assertEqual(data['results'], [])

    def assertReturnJson(self, response):
        self.assertEquals(response.status_code, 200)
        data = response.json()
        self.assertEquals(data['count'], 2)

    def assertNotReally(self, path: str):
        response = self.client.get(path=path)
        self.assertEquals(response.status_code, 404)


# ___________________________________________Pols________________________________________

class QuestionsAPITest(BaseAPITestCase):

    def test_empty_questions(self):
        self.assertEmptyResponse('/api/questions/')

    def test_return_json_questions(self):
        response = super().get_response_with_db(path='/api/questions/', model=Question)
        self.assertReturnJson(response=response)

    def test_not_really_question(self):
        self.assertNotReally('/api/questions/1/')

    def test_return_detail_questions(self):
        response = super().get_response_with_db(path='/api/questions/', model=Question)
        data = response.json()

        self.assertEqual(data['results'][0]['question_text'], 'Hello')
        self.assertEqual(data['results'][1]['question_text'], 'Its me')
        self.assertEqual(data['results'][0]['choices'][0]['choice_text'], 'Privet')
        self.assertEqual(data['results'][1]['choices'][0]['choice_text'], 'Always me')


class ChoicesAPITest(BaseAPITestCase):
    def test_empty_choices(self):
        self.assertEmptyResponse('/api/choices/')

    def test_return_json_choices(self):
        response = super().get_response_with_db(path='/api/choices/', model=Choice)
        self.assertReturnJson(response=response)

    def test_not_really_choices(self):
        self.assertNotReally('/api/choices/1/')

    def test_return_detail_choice(self):
        response = super().get_response_with_db(path='/api/choices/', model=Choice)
        self.assertReturnJson(response=response)
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
        response = super().get_response_with_db(path='/api/articles/', model=Article)
        self.assertReturnJson(response=response)

    def test_not_really_article(self):
        self.assertNotReally('/api/article/1/')

    def test_return_detail_articles(self):
        response = super().get_response_with_db(path='/api/articles/', model=Article)
        self.assertReturnJson(response=response)
        data = response.json()

        self.assertEqual(data['results'][0]['author'], 1)  # Question.pk
        self.assertEqual(data['results'][1]['author'], 2)  # Question.pk
        self.assertEqual(data['results'][0]['title'], 'Jinja')
        self.assertEqual(data['results'][1]['title'], 'I and zavod')
        self.assertEqual(data['results'][0]['content'], 'Jinja - top')
        self.assertEqual(data['results'][1]['content'], 'Love')


# _______________________________________Shop___________________________________________
class ProductAPItest(BaseAPITestCase):

    def test_empty_shop_products(self):
        self.assertEmptyResponse('/api/products/')

    def test_return_json_shop_products(self):
        response = super().get_response_with_db(path='/api/products/', model=Product)
        self.assertReturnJson(response=response)

    def test_not_really_products(self):
        self.assertNotReally('/api/products/1/')

    def test_return_detail_products(self):
        response = super().get_response_with_db(path='/api/products/', model=Product)
        self.assertReturnJson(response=response)
        data = response.json()

        self.assertEqual(data['results'][0]['product_name'], 'Iphone')
        self.assertEqual(data['results'][0]['description'], 'top')
        self.assertEqual(data['results'][0]['price'], 100)

        self.assertEqual(data['results'][1]['product_name'], 'Asus')
        self.assertEqual(data['results'][1]['description'], 'for gaming')
        self.assertEqual(data['results'][1]['price'], 110)


class CategoryAPITest(BaseAPITestCase):

    def test_empty_shop_category(self):
        self.assertEmptyResponse('/api/categories/')

    def test_return_json_shop_category(self):
        response = super().get_response_with_db(path='/api/categories/', model=Product)
        self.assertReturnJson(response=response)

    def test_not_really_category(self):
        self.assertNotReally('/api/categories/1/')

    def test_return_detail_category(self):
        response = super().get_response_with_db(path='/api/categories/', model=Product)
        self.assertReturnJson(response=response)
        data = response.json()

        self.assertEqual(data['results'][0]['products'][0]['product_name'], 'Iphone')
        self.assertEqual(data['results'][0]['products'][0]['description'], 'top')
        self.assertEqual(data['results'][0]['products'][0]['price'], 100)

        self.assertEqual(data['results'][1]['products'][0]['product_name'], 'Asus')
        self.assertEqual(data['results'][1]['products'][0]['description'], 'for gaming')
        self.assertEqual(data['results'][1]['products'][0]['price'], 110)
