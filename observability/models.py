from django.db import models
from django.contrib.auth.models import User

class Meeting(models.Model):
    title = models.CharField(max_length=255)
    scheduled_at = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meetings_created')
    participants = models.ManyToManyField(User, related_name='meetings_joined', blank=True)

    def __str__(self):
        return f"{self.title} ({self.scheduled_at})"


class Message(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
