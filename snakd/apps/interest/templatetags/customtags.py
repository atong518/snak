from django import template
import json

register = template.Library()

@register.filter(name='loadsjs')
def loadsjs(value):
	return json.loads(value)

@register.filter(name='dumpsjs')
def loadsjs(value):
	return json.dumps(value)