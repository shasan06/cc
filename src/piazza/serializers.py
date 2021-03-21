from django.conf import settings
from rest_framework import serializers


MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
from .models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['message']
    #the thing which is not the same is the clean and validate. the actual value that is being passed into that field

    def validate_content(self, value):# message to value and forms to serializers are changed
        if len(value) > MAX_TWEET_LENGTH: #max_.. is imported  now from settings django.conf
            raise serializers.ValidationError("This tweet is too long")
        return value
