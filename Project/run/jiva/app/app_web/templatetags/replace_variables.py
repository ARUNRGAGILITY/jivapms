from django import template
from markdownx.utils import markdownify
from django.template import Template, Context


register = template.Library()

@register.filter(name='replace_variables')
def replace_variables(value, context):
    return value.format(**context)
