from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

router = routers.DefaultRouter()
router.register('questions', views.QuestionViewSet)
router.register('choices', views.ChoiceViewSet)
router.register("articles", views.ArticleViewSet)
router.register("categories", views.CategoryViewSet)
router.register("products", views.ProductViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('questions/<int:question_id>/vote', views.choice_vote),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', views.RegistrtionUserView.as_view(), name='registration'),
    path('add_to_cart/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', views.CartView.as_view(), name='my_cart'),
    path('cart/update/', views.UpdateCartView.as_view(), name='update_cart'),
    path('complete_order/', views.CompleteCartView.as_view(), name='complete_order'),
    path('current_user/', views.ProfileView.as_view(), name='current_user'),
    path('current_user/orders/', views.LastOrders.as_view(), name='current_user_orders'),
    path('repeat_order/', views.RepeatOrder.as_view(), name='repeat_order'),

]
