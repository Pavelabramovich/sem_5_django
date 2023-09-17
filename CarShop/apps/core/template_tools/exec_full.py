from django import template
from .exec import ExecNode
import re


def exec_full_tag(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(f"{token.contents[0]} tag requires arguments")

    if not arg:
        raise template.TemplateSyntaxError(f"{tag_name} tag at least require one argument")

    return ExecNode(token.contents)
