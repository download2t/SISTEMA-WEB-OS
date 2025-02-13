# Em um arquivo custom_tags.py
from django import template

register = template.Library()

@register.filter
def zip_lists(a, b, c):
    return zip(a, b, c)