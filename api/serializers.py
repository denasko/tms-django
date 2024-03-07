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


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2']


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def create(self, data: dict) -> User:
        user = User.objects.create_user(username=data["username"], email=data["email"],
                                        first_name=data["first_name"], last_name=data["last_name"])
        return user
