from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('add_product', views.add_product, name='add_product'),
    path('feedback', views.feedback, name='feedback'),
    path('<int:product_id>', views.show_product, name='product'),
    path('<str:category_name>', views.show_category, name='category'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('my_cart/', views.my_cart, name='my_cart'),
    path('process_order/', views.process_order, name='process_order'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('remove_entry/', views.remove_entry, name='remove_entry'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('order_history/', views.order_history, name='order_history'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('my_cart/repeat_order/<int:order_id>/', views.repeat_order, name='repeat_order'),
    path('like/<int:product_id>/', views.add_like, name='add_like'),

]