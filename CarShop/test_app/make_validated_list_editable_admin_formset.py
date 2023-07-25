from django.forms import BaseModelFormSet
from django import forms


def make_validated_list_editable_admin_formset(model_form):
    # This class use base method clean() from forms to validation.
    # The type of form objects here is a wrapper over the written ones.
    # However, due to the similar structure and duck typing, you can use them instead of the original ones.
    class AdminFormSet(BaseModelFormSet):
        def clean(self):
            BaseModelFormSet.clean(self)

            non_field_errors = []

            for form in self.forms:
                try:
                    model_form.clean(form)
                except forms.ValidationError as error:
                    if hasattr(error, "error_dict"):
                        for field, message in error.error_dict.items():
                            if not form.has_error(field):
                                form.add_error(field, message)
                    else:
                        non_field_errors.append(error)

            if non_field_errors:
                raise forms.ValidationError(non_field_errors)

    return AdminFormSet
