from django.contrib.auth.models import User
from django.db.models.signals import post_init, pre_save, post_save, pre_init
from django.dispatch import receiver

from .models import Order, Profile


@receiver(post_save, sender=User)
def verify_user_profile_is_created(instance: User, created: bool, **kwargs):
    if created:
        instance.profile = Profile.objects.create(user=instance)
        instance.save()


@receiver(post_save, sender=Profile)
def verify_user_profile_shopping_cart_is_set(instance: Profile, created: bool, **kwargs):
    if created:
        instance.shopping_cart = Order.objects.create(profile=instance)
        instance.save()
