from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.contrib.auth.models import User, Permission
from django.dispatch import receiver

from .validators import is_valid, validate_provider


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(pre_delete, sender=User)
def delete_profile(sender, instance, **kwargs):
    instance.profile.delete()


def get_user_permissions(user):
    if user.is_superuser:
        return Permission.objects.all()
    return user.user_permissions.all() | Permission.objects.filter(group__user=user)



def validate_providers(sender, **kwargs):
    instance = kwargs.pop('instance', None)

    print(f"SAVE perm SIGNAL {instance.username}")
    print(get_user_permissions(instance))

    if not is_valid(validate_provider)(instance) and instance.products.count() > 0:
        instance.products.clear()
        instance.save()


@receiver(m2m_changed, sender=User.user_permissions.through)
@receiver(m2m_changed, sender=User.groups.through)
def validate(sender, **kwargs):
    if kwargs.get('action') in ('post_add', 'post_remove'):
        instance = kwargs.pop('instance', None)

        if not is_valid(validate_provider, instance) and instance.products.count() > 0:
            instance.products.clear()
            instance.save()



