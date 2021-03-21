import random
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import TweetForm
from .models import Tweet #Here Piazza is a Tweet which is a class in models

ALLOWED_HOSTS = settings.ALLOWED_HOSTS
# Create your views here.
def home_view(request, *args, **kwargs):
    #print(request.user or None) #associate a user in this view
    #print(args, kwargs) no need any more
    # return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/home.html", context={}, status=200)


def tweet_create_view(request, *args, **kwargs):
    '''
    REST API Create View->DRF(Django rest framework)
    '''
    user = request.user
    if not request.user.is_authenticated:#if the user pass this block which applies that they are authenticated which the applies one can use obj.user
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    #server define
    #print(abc)
    #print("ajax", request.is_ajax())
    form = TweetForm(request.POST or None)
    #print('post data is', request.POST)
    next_url = request.POST.get("next") or None
    #print("next_url", next_url)
    if form.is_valid():
        obj = form.save(commit=False)
        #do other form related logic
        obj.user = user #user or None # None Annon User then it will default to none
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 == created items, no need of print ajax statement as we have this

        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})


def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/ioS/Android
    return json data
    """

    qs = Tweet.objects.all()#looping through all of the objects in the database
    #tweets_list = [{"id": x.id, "message": x.message, "likes": random.randint(0, 122)} for x in qs]#turning python obj into dictionary
    tweets_list = [x.serialize() for x in qs]#just do serialise instead of returning dict
    data = {
        "isUser": False,
       "response": tweets_list
    }
    return JsonResponse(data)


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/ioS/Android
    return json data
    """

    data = {
        "id": tweet_id,
        #"message": obj.message,
        #"image_path": obj.image.url
    }
    status = 200
    try:
    #print(args, kwargs) used for testing 
        obj = Tweet.objects.get(id=tweet_id)
        data['message'] = obj.message #if there is an object then add in the object
    except:
        data['message'] = "Not found"
        status = 404
        #raise Http404
    return JsonResponse(data, status=status) #json.dumps content_type='application/json'
    #return HttpResponse(f"<h1>Hello {tweet_id} - {obj.message}</h1>")