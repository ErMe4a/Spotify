from django.db import models
from account.models import CustomUser
from category.models import Category
from django.db.models.signals import post_save
from spotify.tasks import send_beat_email
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

class Music(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='music')
    image =models.ImageField(upload_to='images/',)
    song = models.FileField(upload_to='mp3/',)
    creator = models.ForeignKey(User,on_delete=models.CASCADE, related_name='music')


    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

@receiver(post_save, sender = Music)
def music_post_save(sender,instance, *args, **kwargs):
    send_beat_email(instance.creator,instance.id)

    
