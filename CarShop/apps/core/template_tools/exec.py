from django import template
import re


class ExecNode(template.Node):
    def __init__(self, tag_arg):
        self.tag_arg = tag_arg

    def render(self, context):
        clist = list(context)

        clist.reverse()
        context_dict = {}

        for c in clist:
            context_dict.update(c)

            for item in c:
                if isinstance(item, dict):
                    context_dict.update(item)

        try:
            exec_locals = {}
            exec(self.tag_arg, context_dict, exec_locals)

        except IndentationError as e:
            raise

        except SyntaxError as e:
            raise SyntaxError(
                "Make sure you don't use special dot notation and other quirks of template syntax.") from e

        else:
            for key, value in exec_locals.items():
                context[key] = value

            return ''


def exec_tag(parser, token):
    try:
        exec_tag_pattern = r"exec\n?"
        tag_arg = re.sub(exec_tag_pattern, '', token.contents, 1, re.M)

        indent_end = next(idx for idx, char in enumerate(tag_arg) if not char.isspace())
        indent = tag_arg[:indent_end]
        indent_pattern = f"^{indent}"

        tag_arg = re.sub(indent_pattern, '', tag_arg, 0, re.M)

    except ValueError:
        raise template.TemplateSyntaxError(f"{token.contents[0]} tag requires arguments")

    return ExecNode(tag_arg)
