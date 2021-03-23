from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Tweet
# Create your tests here.
User = get_user_model()

class TweetTestCase(TestCase):#Inherit test case
    def setUp(self):
        #User.objects.create_user(username='abc', password='somepassword')
        self.user = User.objects.create_user(username='cfe', password='somepassword')
        Tweet.objects.create(message="my first tweet", user=self.user)
        Tweet.objects.create(message="my first tweet", user=self.user)
        Tweet.objects.create(message="my first tweet", user=self.user)


    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(message="my second tweet", user=self.user)
        self.assertEqual(tweet_obj.id, 4)#id of 4 because 3 are created up and the 4th one here
        self.assertEqual(tweet_obj.user, self.user)
    '''def test_user_created(self):
        #user = User.objects.get(username="cfe")
        self.assertEqual(self.user.username, "cfe")
        self.assertEqual(1, 2)'''

        #test the urls django rest framework testing -- find in api guide for testing


    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/piazza/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        #print(response.json())

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/piazza/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/piazza/action/", 
            {"id": 1, "action": "likes"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)

    #for dislike
    def test_action_dislike(self):
        client = self.get_client()
        response = client.post("/api/piazza/action/", 
            {"id": 2, "action": "likes"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/piazza/action/", 
            {"id": 2, "action": "dislikes"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)
        #print(response.json())
        #self.assertEqual(len(response.json()), 3)
        #got an error when testing unlike eg None!=0 means app is not sending back the data
    
    #for comments/retweeting
    def test_action_comment(self):
        client = self.get_client()
        response = client.post("/api/piazza/action/", 
            {"id": 2, "action": "comments"})
        self.assertEqual(response.status_code, 201)