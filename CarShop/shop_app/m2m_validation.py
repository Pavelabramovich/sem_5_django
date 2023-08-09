import operator

from django.db.models import BLANK_CHOICE_DASH

from .models import Product
from .static_init import static_init
from django.utils.functional import classproperty
from django import forms
from django.db.models.fields.related import ManyToManyField
from more_admin_filters import MultiSelectRelatedFilter, MultiSelectFilter

from .validators import to_condition


def m2m_validation(fields_validators_dict):
    def _wrapper(modelform):
        class M2MValidatedModelForm(modelform):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                if self.instance.pk:
                    for field in fields_validators_dict:
                        initial_field_values = getattr(self.instance, field).values_list('pk', flat=True)
                        self.initial[field] = initial_field_values

            def save(self, *args, **kwargs):
                kwargs['commit'] = True
                return super().save(*args, **kwargs)

            def save_m2m(self):
                for field in fields_validators_dict:
                    getattr(self.instance, field).clear()
                    getattr(self.instance, field).add(*self.cleaned_data[field])

        def _get_m2m_field_replacement(field, validators):
            all_field_values = modelform.base_fields[field].queryset
            filtered_fields_values = all_field_values

            for validator in validators:
                filtered_fields_values = filtered_fields_values.condition_filer(to_condition(validator))

            return forms.ModelMultipleChoiceField(
                queryset=filtered_fields_values,
                required=False,
            )

        for field, validators in fields_validators_dict.items():
            setattr(M2MValidatedModelForm, field, _get_m2m_field_replacement(field, validators))

        return M2MValidatedModelForm

    return _wrapper


def get_filtered_filter(validator):
    class Fil(MultiSelectRelatedFilter):
        def field_choices(self, field, request, model_admin):
            ordering = self.field_admin_ordering(field, request, model_admin)
            return self._get_field_choices(field, include_blank=False, ordering=ordering)

        @staticmethod
        def _get_field_choices(
            field,
            include_blank=True,
            blank_choice=BLANK_CHOICE_DASH,
            limit_choices_to=None,
            ordering=(),
        ):
            if field.choices is not None:
                choices = list(field.choices)
                if include_blank:
                    blank_defined = any(
                        choice in ("", None) for choice, _ in field.flatchoices
                    )
                    if not blank_defined:
                        choices = blank_choice + choices
                return choices

            rel_model = field.remote_field.model
            limit_choices_to = limit_choices_to or field.get_limit_choices_to()
            choice_func = operator.attrgetter(
                field.remote_field.get_related_field().attname
                if hasattr(field.remote_field, "get_related_field")
                else "pk"
            )
            qs = rel_model._default_manager.complex_filter(limit_choices_to)
            if ordering:
                qs = qs.order_by(*ordering)

            qs = qs.condition_filter(to_condition(validator))

            return (blank_choice if include_blank else []) + [
                (choice_func(x), str(x)) for x in qs
            ]

    return Fil


def m2m_validated_admin(fields_validators_dict):
    def _wrapper(admin_class):
        # print(self.__dict__['model'].__dict__['providers'].__dict__['field'].__dict__['choices'])

        print(admin_class.__dict__)

        # admin_class.model = type('NewModel', admin_class.model, {})
        #
        # for field, validator in fields_validators_dict.items():
        #     field = getattr(admin_class.model, field)
        #     field.choices = _get_field_choices(field, validator)

        return admin_class

    @staticmethod
    def _get_field_choices(
        field,
        validator,
        include_blank=True,
        blank_choice=BLANK_CHOICE_DASH,
        limit_choices_to=None,
        ordering=(),
    ):
        rel_model = field.remote_field.model
        limit_choices_to = limit_choices_to or field.get_limit_choices_to()
        choice_func = operator.attrgetter(
            field.remote_field.get_related_field().attname
            if hasattr(field.remote_field, "get_related_field")
            else "pk"
        )
        qs = rel_model._default_manager.complex_filter(limit_choices_to)
        if ordering:
            qs = qs.order_by(*ordering)

        qs = qs.condition_filter(to_condition(validator))

        return (blank_choice if include_blank else []) + [
            (choice_func(x), str(x)) for x in qs
        ]

    return _wrapper
