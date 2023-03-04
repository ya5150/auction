from django import template
from .sets import sets

register = template.Library()

register.simple_tag(name="sets")(sets)
