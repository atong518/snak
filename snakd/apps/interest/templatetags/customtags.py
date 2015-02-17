from django import template

register = template.Library()

@register.filter(name='loadsjs')
def loadsjs(value):
	import json
	return json.loads(value)

@register.filter(name='dumpsjs')
def loadsjs(value):
	import json
	return json.dumps(value)