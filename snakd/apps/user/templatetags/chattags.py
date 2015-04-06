from django import template
import json

register = template.Library()

@register.filter(name='userlist')
def userlist(thread, currentuser):
	userlist = []
	for user in thread.members.all():
		if user.email != currentuser.email:
			userlist.append(user.get_fullname())
	return userlist

@register.filter(name='joinby')
def joinby(value, arg):
    return arg.join(value)