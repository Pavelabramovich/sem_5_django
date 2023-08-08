from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(pre_delete, sender=User)
def delete_profile(sender, instance, **kwargs):
    instance.profile.delete()

