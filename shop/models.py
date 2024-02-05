from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    category_name = models.CharField(max_length=200)
    objects: QuerySet

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    like_count = models.IntegerField(default=0)
    sale = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')
    objects: QuerySet

    def __str__(self):
        return self.product_name


class OrderEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_entry')
    count = models.IntegerField(default=0, blank=False)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_entries')
    objects: QuerySet

    def __str__(self):
        return f'{self.product} - {self.count}'


class Order(models.Model):
    class Status(models.TextChoices):
        INITIAL = "IN", _("INITIAL")
        COMPLETED = "CP", _("COMPLETED")
        DELIVERED = "DL", _("DELIVERED")

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=2, choices=Status, default=Status.INITIAL)
    objects: QuerySet


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shopping_cart = models.OneToOneField(Order, on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='shopping_cart')
    objects: QuerySet

    def __str__(self):
        return f"Profile: {self.user.username}"
