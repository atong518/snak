from snakd.apps.user.models import *
from snakd.apps.chat.models import *

users = CollegeUser.objects.filter(email__contains=".15@")

for user in users:
	threads = Thread.objects.filter(members__contains=user)
	for thread in threads:
		messages = Message.objects.filter(thread=thread)
		messages.delete()
	threads.delete()

users.delete()