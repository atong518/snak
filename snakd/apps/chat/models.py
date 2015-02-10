from django.db import models
from django.db.models import signals
from django.utils import timezone
from snakd.apps.user.models import GenericUser

class Thread(models.Model):
    members = models.ManyToManyField(GenericUser)
    subject = models.CharField(max_length=200)
    started_at = models.DateTimeField("started at" , null=True, blank=True)

    def __str__(self):
        return self.subject

class Message(models.Model):
    """
    A private message from user to user
    """
    thread = models.ForeignKey(Thread)
    text = models.TextField()
    sender = models.ForeignKey(GenericUser, related_name='sent_messages', verbose_name="Sender")
    sent_at = models.DateTimeField("sent at", null=True, blank=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-sent_at']
