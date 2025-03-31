# yourapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def kanban_column_count(columns, column_type):
    return sum(1 for column in columns if column.column_type == column_type)
