from django.db.models import signals

from polls.models import Question


def my_callback(sender, instance, created):
    print(f'Pre save. Sender: {sender}, instance: {instance}, created: {created}')


signals.post_save.connect(my_callback, sender=Question)
