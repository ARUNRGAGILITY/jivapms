from django import template

register = template.Library()

@register.filter
def format_time(time_value):
    if time_value is None:
        return ""
    if isinstance(time_value, str):
        return ""

    if isinstance(time_value, int):
        if time_value >= 3600:
            hours, remainder = divmod(time_value, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f'{hours} hrs {minutes} mins {seconds} secs'
        elif time_value >= 60:
            minutes, seconds = divmod(time_value, 60)
            return f'{minutes} mins {seconds} secs'
        else:
            return f'{time_value} secs'

    hours, remainder = divmod(time_value.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'