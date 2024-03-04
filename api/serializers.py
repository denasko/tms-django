from rest_framework import serializers

from articles.models import Article
from polls.models import Question, Choice
from shop.models import Product, Category, User, OrderEntry, Order


# Polls
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


# Articles
class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


# Shop
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class CategorySerializerWithoutProducts(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['Product']


class OrderEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderEntry
        fields = '__all__'
        exclude = ['Product']


class OrderSerializer(serializers.ModelSerializer):
    order_entryes = OrderEntrySerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['Product']


class UpdateOrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    remove = serializers.BooleanField(required=False, default=False)
    count = serializers.IntegerField(required=False, default=None, allow_null=True)