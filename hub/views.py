from django.shortcuts import render, redirect
from .models import User

def index(request):
    # print(request.user.get_group_permissions())
    if request.user.has_perm('hub.add_movie'):
        print('hey')
        pass
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
