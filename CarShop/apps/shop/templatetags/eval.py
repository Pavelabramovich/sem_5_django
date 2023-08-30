from django import template
from django.utils.translation import gettext_lazy as _
import re


register = template.Library()


class EvalNode(template.Node):
    def __init__(self, eval_string, var_name):

        self.eval_string = eval_string
        self.var_name = var_name

    def render(self, context):
        try:
            clist = list(context)

            clist.reverse()
            d = {'_': _}

            for c in clist:
                d.update(c)

                for item in c:
                    if isinstance(item, dict):
                        d.update(item)

            if self.var_name:
                context[self.var_name] = eval(self.eval_string, d)
                return ''
            else:
                return str(eval(self.eval_string, d))

        except:
            raise


r_eval = re.compile(r'(.*?)\s+as\s+(\w+)', re.DOTALL)


def do_eval(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(f"{token.contents[0]} tag requires arguments")

    m = r_eval.search(arg)
    if m:
        eval_string, var_name = m.groups()
    else:
        if not arg:
            raise template.TemplateSyntaxError(f"{tag_name} tag at least require one argument")

        eval_string, var_name = arg, None

    return EvalNode(eval_string, var_name)


do_eval = register.tag('eval', do_eval)
