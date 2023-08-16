from django import template

register = template.Library()

@register.filter(name='keys')
def keys(value):
    if isinstance(value, dict):
        return value.keys()
    return None
