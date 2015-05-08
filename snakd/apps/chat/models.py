from django.db import models
from django.db.models import signals
from django.utils import timezone
from snakd.apps.user.models import GenericUser
from datetime import datetime

class ThreadManager(models.Manager):
    def in_a_number_order(self, *args, **kwargs):
        qs = self.get_queryset().filter(*args, **kwargs)
        try:
            new = sorted(qs, key=lambda n: (n.message_set.first().timestamp, n.message_set.first().timestamp))
            return new
        except:
            return qs

class Thread(models.Model):
    members = models.ManyToManyField(GenericUser)
    subject = models.CharField(max_length=200, blank=True, default="")
    started_at = models.DateTimeField("started at" , null=True, blank=True, default=datetime.now())
    timestamp = models.BigIntegerField(null=True)
    objects = ThreadManager()

    def __unicode__(self):
        return self.subject

    def mostRecentMessage(self):
        return self.message_set.last().timestamp

    def mostRecentMessageRef(self):
        return self.message_set.last()


class Message(models.Model):
    """
    A private message from user to user
    """
    thread = models.ForeignKey(Thread)
    text = models.TextField()
    sender = models.ForeignKey(GenericUser, related_name='sent_messages', verbose_name="Sender")
    timestamp = models.BigIntegerField(null=True)

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['timestamp']
