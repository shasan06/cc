from django import forms


from .models import Tweet

MAX_TWEET_LENGTH = 240

class TweetForm(forms.ModelForm):
    #can also declare individuals fields like below
    #message = forms.TextFeld()
    class Meta:
        model = Tweet
        fields = ['message']

    #message will be cleaned and is not over a certain length
    def clean_message(self):
        message = self.cleaned_data.get("message")
        if len(message) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This tweet is too long")
        return message
