from django import template
from graph.models import Spectr

register = template.Library()

@register.simple_tag
def get_spectrs():
    return Spectr.objects.all()