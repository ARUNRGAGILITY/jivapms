from django import template
from markdownx.utils import markdownify
from django.template import Template, Context
from datetime import timedelta

register = template.Library()

@register.filter(name='render_markdown')
def render_markdown(text):
    return markdownify(text)

register = template.Library()

@register.filter(name='replace_variables')
def replace_variables(value, context):
    return value.format(**context)

register = template.Library()

@register.simple_tag(takes_context=True)
def render_markdown_with_context(context, content):
    # Preprocess the content by expanding variables in the context
    preprocessed_content = content.format(**context)
    # Apply markdownify to the preprocessed content
    markdown_output = markdownify(preprocessed_content)
    return markdown_output
register = template.Library()

@register.filter(name='markdown_with_context')
def markdown_with_context(value, context):
    template = Template(value)
    expanded_text = template.render(Context(context))
    return markdownify(expanded_text)



@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='get_value')
def get_value(dictionary, key):
    """Retrieve value from a dictionary using a variable key."""
    return dictionary.get(key, '')


# @register.simple_tag
# def get_nested_value_from_keys(dictionary, *keys):
#     for key in keys:
#         if isinstance(dictionary, dict):
#             print(f"Key: {key}")
#             dictionary = dictionary.get(key, {})
#             print(f"Dictionary: {dictionary}")
#         else:
#             return ''  # Return empty if path breaks
#     return dictionary if not isinstance(dictionary, dict) else ''


@register.simple_tag
def get_nested_value_from_keys(dictionary, *keys):
    for key in keys:
        if isinstance(dictionary, dict):
            dictionary = dictionary.get(key, {})
        else:
            return ''  # Return empty if path breaks
    return dictionary if not isinstance(dictionary, dict) else ''

@register.simple_tag
def date_range(start_date, end_date):
    delta = end_date - start_date
    return [(start_date + timedelta(days=i)) for i in range(delta.days + 1)]