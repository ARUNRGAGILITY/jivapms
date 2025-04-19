from django import template

register = template.Library()

@register.filter
def div(value, arg):
    """Division filter for templates"""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def mul(value, arg):
    """Multiplication filter for templates"""
    try:
        return float(value) * float(arg)
    except ValueError:
        return 0
    
@register.filter
def subtract(value, arg):
    """Subtraction filter for templates"""
    try:
        return value - arg
    except (ValueError, TypeError):
        return 0