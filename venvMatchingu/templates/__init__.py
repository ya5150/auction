from django import template

register = template.Library()

@register.simple_tag
def sets(var_name, var_value):
    return var_value
