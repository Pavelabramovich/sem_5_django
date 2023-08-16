from django.forms.widgets import CheckboxInput


# This widget is needed to create an empty field in which only the label will be visible.
# This is achieved by removing the checkbox icon using css
class LabelOnlyWidget(CheckboxInput):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {'class': 'hidden-checkbox'}
        else:
            attrs['class'] = 'hidden-checkbox'

        super().__init__(attrs)

    class Media:
        css = {
            'all': ('css/hidden_checkbox.css',)
        }
