from django import template
from django.utils.translation import gettext_lazy as _
import re


class EvalNode(template.Node):
    def __init__(self, eval_string, var_name):
        self.eval_string = eval_string
        self.var_name = var_name

    def render(self, context):
        clist = list(context)

        clist.reverse()
        context_dict = {'_': _}

        for c in clist:
            context_dict.update(c)

            for item in c:
                if isinstance(item, dict):
                    context_dict.update(item)

        try:
            if self.var_name:
                context[self.var_name] = eval(self.eval_string,  context_dict)
                return ''
            else:
                return str(eval(self.eval_string,  context_dict))

        except SyntaxError as e:
            raise SyntaxError(
                "Make sure you don't use special dot notation and other quirks of template syntax.") from e


tag_with_as_regex = re.compile(r'(.*?)\s+as\s+(\w+)', re.DOTALL)


def eval_tag(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(f"{token.contents[0]} tag requires arguments")

    if match := tag_with_as_regex.search(arg):
        eval_string, var_name = match.groups()
    else:
        if not arg:
            raise template.TemplateSyntaxError(f"{tag_name} tag at least require one argument")

        eval_string, var_name = arg, None

    return EvalNode(eval_string, var_name)
