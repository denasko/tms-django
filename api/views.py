from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets, filters, views, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from articles.models import Article
from polls.models import Question, Choice
from shop.models import Category, Product, Order, OrderEntry
from . import serializers
from .filters import MinChoiceCountFilter, MaxChoiceCountFilter, MinArticleTextLength
from .pagination import DefaultPagination
from .serializers import QuestionSerializer, ChoiceSerializer, CategorySerializerWithoutProducts, CategorySerializer, \
    OrderSerializer, UpdateOrderSerializer


# ________________________________Polls________________________________________
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = DefaultPagination

    filter_backends = [MinChoiceCountFilter, MaxChoiceCountFilter, filters.OrderingFilter, filters.SearchFilter]

    search_fields = ["id", "question_text", "pub_date"]


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    pagination_class = DefaultPagination
    filter_backends = [MinChoiceCountFilter, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["id", "choice_text", "question__question_text"]


@api_view(['POST'])
def choice_vote(request: Request, question_id: int) -> str:
    question = get_object_or_404(Question, pk=question_id,publication=True)
    selected_choice = get_object_or_404(question.choices, id=request.data['choice'])
    selected_choice.votes += 1
    selected_choice.save()
    return redirect('question-detail', question_id)


# ________________________________Articles________________________________________
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('id')
    serializer_class = serializers.ArticlesSerializer
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter, MinArticleTextLength]
    search_fields = ["id", "title", "authors__first_name", "authors__last_name"]


# ________________________________Shop________________________________________
class CategoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Category.objects.all().order_by('id')
    # serializer_class = serializers.CategorySerializer
    pagination_class = DefaultPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["id", "name"]

    def get_serializer_class(self):
        if self.request.query_params.get('include_products') == 'false':
            return CategorySerializerWithoutProducts
        return CategorySerializer


class ProductViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = serializers.ProductSerializer
    pagination_class = DefaultPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["id", "name"]


# class AddToCartView(views.APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request: Request):
#         product_id = request.data.get('product_id')
#         profile = request.user.profile
#         if not product_id:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         product = get_object_or_404(Product, id=product_id)
#         request.user.profile.shopping_cart  # TODO add to cart
#         return Response(status=status.HTTP_200_OK)

class AddToCartView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)
        profile = request.user.profile

        if not profile.shopping_cart:
            order = Order.objects.create(profile=profile)
            profile.shopping_cart = order
            profile.save()
        else:
            order = profile.shopping_cart

        order_entry, created = OrderEntry.objects.get_or_create(order=order, product=product)
        if not created:
            order_entry.count += 1
            order_entry.save()

        return Response(status=status.HTTP_200_OK)


class CartView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        return Response(OrderSerializer(request.user.profile.shopping_cart).data)


class UpdateCartView(views.APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request: Request):
        update_order = UpdateOrderSerializer(data=request.data)
        update_order.is_valid(raise_exceprion=True)

        order: Order = request.user.profile.shopping_cart
        update_order_data: dict = update_order.validated_data
        self._update_order(order, update_order_data)
        return Response(OrderSerializer(order).data)

    def _update_order(self, order: Order, update_order_data: dict):
        if update_order_data['clear']:
            order.order_entries.all().delete()
        else:
            for update_order_entry_data in update_order_data['order_entries']:
                self._update_order_entry(order, update_order_entry_data)

    def _update_order_entry(self, order: Order, update_order_entry_data: dict):
        order_entry_id = update_order_entry_data['id']
        order_entry = order.order_entries.filter(id=order_entry_id).first()
        if order_entry is None:
            raise ValidationError(f'Unknow order entry id {order_entry_id}')
        if update_order_entry_data['remove']:
            order_entry.delete()
        elif update_order_entry_data['count'] is not None:
            order_entry.count = update_order_entry_data['count']
            order_entry.save()


class CompleteCartView(views.APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request: Request):
        profile = request.user.profile
        order = Order.objects.create(profile=profile, status=Order.Status.COMPLETED)
        if profile.shopping_cart.order_entries.exists():
            entries = profile.shopping_cart.order_entries.all()
            for entry in entries:
                order.order_entries.create(product=entry.product, count=entry.count)
            profile.shopping_cart.order_entries.all().delete()

