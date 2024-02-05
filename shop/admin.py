from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Product, Category, Profile, Order, OrderEntry


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'shopping_cart']


class ProductInline(admin.StackedInline):
    model = Product
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = [
        'product_name', 'description', 'category', 'price',
        'sale', 'like_count', 'is_published', 'pub_date'
    ]
    search_fields = ['product_name']
    list_per_page = 10

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]


@admin.register(OrderEntry)
class OrderEntryAdmin(admin.ModelAdmin):
    list_display = ['product', 'count', 'order']


class OrderEntryInline(admin.TabularInline):
    model = OrderEntry


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['profile', 'status']
    inlines = [OrderEntryInline]