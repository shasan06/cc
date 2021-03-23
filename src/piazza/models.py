import random
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #many users can many tweets(assigning each tweet to a user)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE) #many users can many tweets(assigning each tweet to a user)
    timestamp = models.DateTimeField(auto_now_add=True)

# Create your models here.
class Tweet(models.Model):
    #Maps to SQL data
    #id = models.AutoField(primary_key=True)
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE) #many users can many tweets(assigning each tweet to a user)
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)
    message = models.TextField(blank=True, null=True)
    image   = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    #def __str__(self):string rep of the actual obj itself
    #   return self.message

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return{
            "id": self.id,
            "message": self.message,
            "likes": random.randint(0, 200)
        }