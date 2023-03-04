# myapp/templatetags/my_tags.py

from django import template

register = template.Library()

@register.simple_tag
def my_simple_tag():
    return "This is a simple tag!"
