from django.db.models.signals import pre_delete, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver

from .validators import is_valid, validate_provider


@receiver(pre_delete, sender=User)
def on_user_pre_delete(sender, instance, **kwargs):
    instance.profile.delete()


@receiver(m2m_changed, sender=User.user_permissions.through)
@receiver(m2m_changed, sender=User.groups.through)
def on_user_permissions_changed(sender, **kwargs):
    print("signal")
    if kwargs.get('action') in ('post_add', 'post_remove'):
        instance = kwargs.pop('instance', None)

        if not is_valid(validate_provider, instance) and instance.products.count() > 0:
            instance.products.clear()
            instance.save()


