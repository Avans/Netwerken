from django.db import models

class ChatMessage(models.Model):
    nickname = models.TextField()
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
