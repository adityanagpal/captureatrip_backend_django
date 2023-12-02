from django import template
from dateutil.relativedelta import relativedelta

register = template.Library()

@register.simple_tag
def secs_to_hhmm(value):    
    value = 0 if value is None else int(value)    
    rt = relativedelta(seconds=value)
    return '{:02d}:{:02d}'.format(int(rt.hours), int(rt.minutes))