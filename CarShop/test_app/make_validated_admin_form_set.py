from django.forms import BaseModelFormSet


def make_validated_admin_form_set(model_form):
    class AdminFormSet(BaseModelFormSet):
        def clean(self):
            for form in self.forms:
                model_form.clean(form)

            return self.cleaned_data

    return AdminFormSet
