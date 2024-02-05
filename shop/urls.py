from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('add_product', views.add_product, name='add_product'),
    path('feedback', views.feedback, name='feedback'),
    path('login', views.login, name='login'),
    path('<int:product_id>', views.show_product, name='product'),
    path('<str:category_name>', views.show_category, name='category'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('my_cart/', views.my_cart, name='my_cart'),
    path('process_order/', views.index, name='process_order'),
    path('clear_cart/', views.index, name='clear_cart'),

]