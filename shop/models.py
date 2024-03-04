from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    sale = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')
    likes = models.ManyToManyField(User, through='Like')
    objects: QuerySet

    def __str__(self):
        return self.product_name

    def total_likes(self):
        return self.likes.count()


class OrderEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_entry')
    count = models.IntegerField(default=1, blank=False)
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
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.INITIAL)
    objects: QuerySet

    def __str__(self):
        return f"Order: {self.pk} - {self.profile.user.username}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shopping_cart = models.OneToOneField(Order, on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='shopping_cart')
    objects: QuerySet

    def __str__(self):
        return f"Profile: {self.user.username}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Product, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
