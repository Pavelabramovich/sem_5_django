from django import template

from .eval import do_eval

register = template.Library()
do_eval = register.tag('eval', do_eval)

