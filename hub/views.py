from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.views import generic

def index(request):
    username = request.user.username
    return render(request, 'hub/index.html',{"username":username})

def signup(request):
    if request.method == "POST":
        # TODO - Implement proper user model
        username = request.POST['username']
        fname = request.POST['fname']
        email = request.POST['email']
        password = request.POST['password']

        myuser = User.objects.create_user(username, email, password)
        myuser.fullname = fname
        myuser.save()
        return redirect('login')

    return render(request, 'hub/authentication/signup.html')

def profile(request, pk=None):
    otherUser = None
    ownProfile = False

    if (pk == request.user.id):
        return redirect('profile')  
    if (pk is not None):
        otherUser = get_object_or_404(User, pk=pk)
    elif (request.user.is_authenticated):
        otherUser = request.user
        ownProfile = True
    else:
        return render(request, 'hub/profile.html', {"user":None})

    avatar = otherUser.avatar.url
    banner = otherUser.banner.url
    parameters = {'otherUser':otherUser.get_username(),
    'isProducer':otherUser.has_perm('hub.add_movie'),
    'avatar':avatar, 
    'banner':banner,
    'ownProfile':ownProfile
    }

    return render(request, 'hub/profile.html', parameters)
        

   