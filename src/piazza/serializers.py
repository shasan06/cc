from django.conf import settings
from rest_framework import serializers
from .models import Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

#another serializer for tweet actions
class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    message = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()# "Like"->"like"
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for tweets")
        return value


class TweetCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweet
        fields = ['id', 'message', 'likes']
    #the thing which is not the same is the clean and validate. the actual value that is being passed into that field
    def get_likes(self, obj):
        return obj.likes.count()
    
    def validate_content(self, value):# message to value and forms to serializers are changed
        if len(value) > MAX_TWEET_LENGTH: #max_.. is imported  now from settings django.conf
            raise serializers.ValidationError("This tweet is too long")
        return value
    

class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)
    #message = serializers.SerializerMethodField(read_only=True)
    #is_comment = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweet
        fields = ['id', 'message', 'likes', 'is_comment', 'parent']
    #the thing which is not the same is the clean and validate. the actual value that is being passed into that field
    def get_likes(self, obj):
        return obj.likes.count()
    
    '''def get_message(self, obj):
        message = obj.message#by default we will use the message from the object itself
        if obj.is_comment:
            message = obj.parent.message
        return message'''
    