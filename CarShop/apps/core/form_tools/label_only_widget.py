from django.forms.widgets import CheckboxInput


class LabelOnlyWidget(CheckboxInput):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {'class': 'hidden-checkbox'}
        else:
            attrs['class'] = 'hidden-checkbox'

        super().__init__(attrs)

    class Media:
        css = {
            'all': ('core/form_tools/css/hidden_checkbox.css',)
        }
