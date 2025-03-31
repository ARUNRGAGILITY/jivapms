from django import template
import markdown as md
from django.template.loader import render_to_string
import os
from django.conf import settings

register = template.Library()

@register.filter(name='contains')
def contains(value, arg):
    """Custom template filter to check if 'arg' is in 'value'."""
    return arg in value

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

@register.filter(name='filter_active')
def filter_active(queryset, attribute='active'):
    """
    Filter a queryset based on the attribute which defaults to 'active'.
    Can be used to dynamically filter any queryset based on a provided attribute.
    """
    # Construct the filter condition dynamically
    filter_condition = {f'{attribute}': True}
    return queryset.filter(**filter_condition)

@register.filter(name='filter_template')
def filter_template(queryset, attribute='template'):
    """
    Filter a queryset based on the attribute which defaults to 'active'.
    Can be used to dynamically filter any queryset based on a provided attribute.
    """
    # Construct the filter condition dynamically
    filter_condition = {f'{attribute}': True}
    return queryset.filter(**filter_condition)

@register.filter(name='filter_instance')
def filter_instance(queryset, attribute='template'):
    """
    Filter a queryset based on the attribute which defaults to 'active'.
    Can be used to dynamically filter any queryset based on a provided attribute.
    """
    # Construct the filter condition dynamically
    filter_condition = {f'{attribute}': False}
    return queryset.filter(**filter_condition)

@register.filter(name='get_capacity')
def get_capacity(capacities, key):
    return capacities.get(key, "")

@register.filter
def multiply_spaces(value, num_spaces=4):
    """Creates a string of spaces multiplied by the node's level for indentation."""
    return '&nbsp;' * (value * num_spaces)

@register.filter(name='font_size')
def font_size(node):
    size = 20 - node.level * 1  # Decrease font size as level increases
    return f"{max(size, 8)}px"  # Ensure minimum size

@register.filter(name='markdown')
def markdown_format(text):
    return md.markdown(text, extensions=['markdown.extensions.fenced_code'])

@register.filter(name='handle_none')
def handle_none(text):
    if text == "None":
        return ""
    return text

@register.filter
def is_list(value):
    return isinstance(value, list)

@register.filter
def order_by_position(queryset):
    return queryset.order_by('position')

@register.filter
def get_next_in_list(value, arg):
    """Returns the next item in a list given the current index."""
    try:
        # Ensure the argument is an integer and within the list index range
        return value[int(arg) + 1]
    except (IndexError, ValueError, TypeError):
        # Return None or default if at end of list or error
        return None
    
@register.filter(name='starts_with')
def starts_with(value, arg):
    """Returns True if the value starts with the arg, False otherwise."""
    if isinstance(value, str):
        return value.startswith(arg)
    return False

@register.filter(name='starts_with_any')
def starts_with_any(value, args):
    """Returns True if the value starts with any of the given args."""
    if isinstance(value, str):
        prefixes = args.split(',')  # Args should be comma-separated
        return any(value.startswith(prefix) for prefix in prefixes)
    return False

@register.simple_tag(takes_context=True)
def include_dynamic(context, template_name):
    return render_to_string(template_name, request=context.request)

@register.filter(name='display_if_not_none')
def display_if_not_none(value):
    """Returns the value if it's not None, otherwise returns an empty string."""
    if value is not None:
        return value
    return ""


@register.simple_tag
def static_exists(static_path):
    full_path = os.path.join(settings.STATIC_ROOT, static_path)
    return os.path.exists(full_path)


# {% load static_tags %}

# {% static_exists 'images/my_image.jpg' as image_exists %}
# {% if image_exists %}
#     <img src="{% static 'images/my_image.jpg' %}" alt="My Image">
# {% endif %}


# 27-11-2024

@register.filter
def split_coords(value, index):
    """Splits a comma-separated string and returns the specified index."""
    try:
        coords = value.split(',')
        return float(coords[index])
    except (ValueError, IndexError):
        return 0

import markdown
from django import template
from django.utils.safestring import mark_safe



@register.filter
def render_markdown(value):
    """
    Converts Markdown text to HTML.
    """
    return mark_safe(markdown.markdown(value, extensions=['extra', 'toc', 'codehilite']))


@register.filter
def get_first_letter_caps(value):
    """Capitalizes only the first character of a string."""
    if isinstance(value, str) and value:
        return value[0].upper() 
    return value


# Mar 03 2025

@register.filter
def replace_underscore(value):
    """Replaces underscores with spaces."""
    return value.replace("_", " ") if isinstance(value, str) else value


@register.filter
def get_attr(obj, attr_name):
    """Fetch an attribute from an object dynamically."""
    return getattr(obj, attr_name, None)



@register.filter(name='lowercase')
def lowercase(value):
    """Converts a string to lowercase"""
    return value.lower() if isinstance(value, str) else value
