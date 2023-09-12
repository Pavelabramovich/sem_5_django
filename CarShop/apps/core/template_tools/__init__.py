from django import template

from .eval import eval_tag
from .exec import exec_tag

# Make django templates multiline
import re
from django.template import base
base.tag_re = re.compile(base.tag_re.pattern, re.DOTALL)


tags = {
    'eval': eval_tag,
    'exec': exec_tag
}

register = template.Library()

for tag_name, tag_func in tags.items():
    register.tag(tag_name, tag_func)

