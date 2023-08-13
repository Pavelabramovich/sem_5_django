from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver

from .validators import is_valid, validate_provider


@receiver(post_save, sender=User)
def on_profile_post_save(sender, instance, **kwargs):
    instance.profile.save()


@receiver(pre_delete, sender=User)
def on_profile_pre_delete(sender, instance, **kwargs):
    instance.profile.delete()


@receiver(m2m_changed, sender=User.user_permissions.through)
@receiver(m2m_changed, sender=User.groups.through)
def validate(sender, **kwargs):
    if kwargs.get('action') in ('post_add', 'post_remove'):
        instance = kwargs.pop('instance', None)

        if not is_valid(validate_provider, instance) and instance.products.count() > 0:
            instance.products.clear()
            instance.save()


