from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Chat(models.Model):
    name = models.CharField(max_length=255)

    participants = models.ManyToManyField(User)
    admin = models.ForeignKey(User, related_name='admin', on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
        # теперь мы можем добавить администратора в участники
        if self.admin not in self.participants.all():
            self.participants.add(self.admin)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True)