from http.client import HTTPResponse
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Follower
from django.views import generic

def index(request):
    username = request.user.username
    return render(request, 'hub/index.html',{"username":username})

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        email = request.POST['email']
        password = request.POST['password']

        myuser = User.objects.create_user(username, email, password)
        myuser.fullname = fname
        myuser.save()
        return redirect('login')

    return render(request, 'hub/authentication/signup.html')

def follow(request):
    if request.method == "POST":
        if(request.user.id == request.POST['id']):
            return HTTPResponse('ID is the same')
        else:
            user = request.user
            id = request.POST['id']
            producer = User.objects.get(pk=id)
            try:
                followExists = Follower.objects.get(producer=producer, follower=user)  
                return redirect(f'/profile/{id}')
            except (KeyError, Follower.DoesNotExist):
                follow = Follower(producer=producer,follower=user)
                follow.save()
                return redirect(f'/profile/{id}')

def unfollow(request):
    if request.method == "POST":
        user = request.user
        id = request.POST['id']
        try:
            producer = User.objects.get(pk=id)
            followExists = Follower.objects.get(producer=producer, follower=user)  
            followExists.delete()
            return redirect(f'/profile/{id}')
        except (KeyError, Follower.DoesNotExist):
            return redirect(f'/profile/{id}')
            

def profile(request, pk=None):
    otherUser = None
    ownProfile = False
    isFollowing = False
    
    if (pk == request.user.id):
        return redirect('profile')  
    if (pk is not None):
        otherUser = get_object_or_404(User, pk=pk)
    elif (request.user.is_authenticated):
        otherUser = request.user
        ownProfile = True
    else:
        return render(request, 'hub/profile.html', {"user":None})

    try:  
        if(request.user.follower.get(producer=otherUser)):
            isFollowing = True
    except(KeyError, Follower.DoesNotExist): 
        isFollowing = False
    avatar = otherUser.avatar.url
    banner = otherUser.banner.url
    parameters = {'otherUser':otherUser.get_username(),
    'otherUserId':otherUser.id,
    'isProducer':otherUser.has_perm('hub.add_movie'),
    'isFollowing':isFollowing,
    'avatar':avatar, 
    'banner':banner,
    'ownProfile':ownProfile
    }

    return render(request, 'hub/profile.html', parameters)
        

   