from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter(name='formatnumber')
def format_number(value, arg=0):
    try:
        rounded_value = round(float(value), arg)
        int_part = intcomma(int(rounded_value))
        if arg > 0:
            return "%s%s" % (int_part, ("%0.2f" % rounded_value)[-3:])
        else:
            return int_part
    except:
        return value

@register.filter(name='formattimediff')
def format_timediff(value):
    try:
        days, remainder = divmod(value, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        if days > 0:
            return "%dd %dh %dmin" % (days, hours, minutes)
        else:
            return "%dh %dmin" % (hours, minutes)
        
    except:
        return value