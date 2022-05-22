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
    if (pk is not None):
        user = get_object_or_404(User, pk=pk)
        return render(request, 'hub/profile.html', {'otherUser':user,'isProducer':user.has_perm('hub.add_movie')})
    if (request.user.is_authenticated):
        user = request.user
        return render(request, 'hub/profile.html')
    else:
        return render(request, 'hub/profile.html', {"user":None})
    
        

   