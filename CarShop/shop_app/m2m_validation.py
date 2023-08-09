import operator

from django.db.models import BLANK_CHOICE_DASH, QuerySet

from .queryset_condition_filter import queryset_condition_filter

from django import forms
from django.db.models.fields.related import ManyToManyField

from .validators import to_condition


QuerySet.condition_filter = queryset_condition_filter


class ValidatedManyToManyField(ManyToManyField):
    def get_choices(
            self,
            include_blank=True,
            blank_choice=BLANK_CHOICE_DASH,
            limit_choices_to=None,
            ordering=(),
    ):
        rel_model = self.remote_field.model
        limit_choices_to = limit_choices_to or self.get_limit_choices_to()
        choice_func = operator.attrgetter(
            self.remote_field.get_related_field().attname
            if hasattr(self.remote_field, "get_related_field")
            else "pk"
        )

        qs = rel_model._default_manager.complex_filter(limit_choices_to)

        for validator in self.validators:
            qs = qs.condition_filter(to_condition(validator))

        if ordering:
            qs = qs.order_by(*ordering)

        return (blank_choice if include_blank else []) + [
            (choice_func(x), str(x)) for x in qs
        ]

    def formfield(self, *, using=None, **kwargs):
        qs = self.remote_field.model._default_manager.using(using)

        for validator in self.validators:
            qs = qs.condition_filter(to_condition(validator))

        defaults = {
            "form_class": forms.ModelMultipleChoiceField,
            **kwargs,
            "queryset": qs,
        }

        if defaults.get("initial") is not None:
            initial = defaults["initial"]
            if callable(initial):
                initial = initial()

            defaults["initial"] = [i.pk for i in initial]

        return super(ManyToManyField, self).formfield(**defaults)

    # Remove warning: ManyToManyField does not support validators
    def _check_ignored_options(self, **kwargs):
        warnings = super()._check_ignored_options(**kwargs)
        return [warning for warning in warnings if warning.id != "fields.W341"]


