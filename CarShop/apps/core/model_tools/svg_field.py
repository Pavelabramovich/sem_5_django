from django.db.models import FileField
from django.core.exceptions import ValidationError

from apps.core.model_tools import NamedFileField
import xml.etree.cElementTree as et


def validate_svg(f):
    # Find "start" word in file and get "tag" from there
    f.seek(0)
    tag = None
    try:
        for event, el in et.iterparse(f, ('start',)):
            tag = el.tag
            break
    except et.ParseError:
        pass

    # Check that this "tag" is correct
    if tag != '{http://www.w3.org/2000/svg}svg':
        raise ValidationError('Uploaded file is not an image or SVG file.')

    # Do not forget to "reset" file
    f.seek(0)

    return f


class SvgField(NamedFileField):
    def __init__(self, *args, **kwargs):
        if 'validators' in kwargs:
            if validate_svg not in kwargs['validators']:
                kwargs['validators'].append(validate_svg)
        else:
            kwargs['validators'] = [validate_svg]

        super().__init__(*args, **kwargs)
