from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

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
        return redirect('login')

    return render(request, 'hub/authentication/signup.html')
