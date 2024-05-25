from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Conversation(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    topic = models.CharField(max_length=128, verbose_name="Conversation Topic")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
    
    def __str__(self):
        return self.topic

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation,on_delete=models.CASCADE)
    body = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
    
    def __str__(self):
        return f"{self.conversation} - {self.sender}"


