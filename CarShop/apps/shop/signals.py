from django.db.models.signals import pre_delete, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver


@receiver(pre_delete, sender=User)
def on_user_pre_delete(sender, instance, **kwargs):
    instance.profile.delete()
