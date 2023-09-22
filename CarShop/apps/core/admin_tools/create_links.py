from django.urls import reverse
from django.utils.html import mark_safe, urlencode


def create_link_one(target, text):
    app_name = target._meta.app_label
    reverse_name = type(target).__name__.lower()

    link = (
        reverse(f"admin:{app_name}_{reverse_name}_change", args=(target.pk,))
        + '?'
        + urlencode({"_changelist_filters": f'id__in={target.pk}'})
    )

    return mark_safe(f"<a href='{link}'>{text}</a>")


def create_link_many(targets, text):
    first = next(iter(targets))

    app_name = first._meta.app_label
    reverse_name = type(first).__name__.lower()

    targets_pk = ','.join([str(obj.pk) for obj in targets])

    link = (
        reverse(f"admin:{app_name}_{reverse_name}_changelist")
        + '?'
        + urlencode({"id__in": targets_pk})
    )

    return mark_safe(f"<a href='{link}'>{text}</a>")
