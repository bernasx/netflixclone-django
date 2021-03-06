from http.client import HTTPResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Follower, Video, View
from django.db.models import Q
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime

def index(request):
    producers = []
    publicVideos = Video.objects.filter(isPublic=True)[:5] # keep this at 5, changing this means changing the banner
    user = request.user
    # gets all the producers that this user follows
    if(user.is_authenticated):
        following = Follower.objects.filter(follower=user)
        for follow in following:
            if(len(follow.producer.video_set.all()) > 0):
                producers.append(follow.producer)

    return render(request, 'hub/index.html', {"producers": producers[:3], "publicVideos":publicVideos})

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

@login_required              
def profile(request, pk=None):
    otherUser = None
    ownProfile = False
    isFollowing = False
    followers = None
    views = None

    if (pk == request.user.id):
        # redirect to /profile/ if we end up in our own profile
        return redirect('profile')  
    if (pk is not None):
        # this is the route /profile/1 or similar, someone else's profile
        otherUser = get_object_or_404(User, pk=pk)
    elif (request.user.is_authenticated):
        # this is the route /profile/ and thus our own profile
        otherUser = request.user
        ownProfile = True
        views = View.objects.filter(viewer=otherUser).order_by('-date')[:5]
    else:
        return render(request, 'hub/profile.html', {"user":None})
    try:  
        if(request.user.follower.get(producer=otherUser)):
            isFollowing = True
    except(KeyError, Follower.DoesNotExist): 
        isFollowing = False
    avatar = otherUser.avatar.url
    banner = otherUser.banner.url


    followers = Follower.objects.filter(follower=otherUser)
    
    parameters = {'otherUser':otherUser,
    'views':views,
    'followers':followers,
    'otherUserId':otherUser.id,
    'isProducer':otherUser.has_perm('hub.add_video'),
    'isFollowing':isFollowing,
    'avatar':avatar, 
    'banner':banner,
    'ownProfile':ownProfile
    }

    return render(request, 'hub/profile.html', parameters)

@login_required     
def edit_User(request):
    if request.method == "POST" and request.user.is_authenticated:
        
        user = request.user
        user.username = request.POST['username']
        user.fullname = request.POST['fullname']
        user.email = request.POST['email']
        newpassword = request.POST['password']
        checks = request.POST.getlist('checks')
        if('wipeViewHistory' in checks):
            views = View.objects.filter(viewer=user)
            views.delete()

        try:
            if (request.FILES['avatar']):
                user.avatar = request.FILES['avatar']
        except:
            pass

        try:
            if (request.FILES['banner']):
                user.banner = request.FILES['banner']
        except:
            pass

        if (newpassword != ''):
            user.set_password(newpassword)
            user.save()
            return redirect('login')
        else:
            user.save()
            return redirect('profile')
            
    if request.method == "GET" and request.user.is_authenticated:
        return render(request, 'hub/edit_user.html')

def search(request):
    if(request.method == 'GET'):
        searchterm = request.GET['search']
        videos = Video.objects.filter(Q(title__icontains=searchterm) | Q(tag__tag__icontains=searchterm) | Q(producer__username__icontains=searchterm)).distinct()
        users = User.objects.filter(username__icontains=searchterm)
        parameters = {'videos':videos,'users':users}
        return render(request, 'hub/search.html', parameters)

class VideosView(generic.ListView):
    template_name = 'hub/videos/videos.html'
    context_object_name = 'videos_list'

    def get_queryset(self):
        if(self.request.user.is_authenticated):
            return Video.objects.filter(Q(isPublic=True) | Q(isPublic = False,producer=self.request.user))[:20]
        else:
            return Video.objects.filter(isPublic=True)[:20]

class VideoDetailView(generic.DetailView):
    model = Video
    template_name = 'polls/video_detail.html'

    def get_queryset(self):
        if(self.request.user.is_authenticated):
            # Query where it returns the video if it is public, if it is unlisted or if it is your own video
            return Video.objects.filter(Q(isPublic=True) | Q(isUnlisted=True) |Q(isPublic = False,producer=self.request.user))
        else:
            return Video.objects.filter(Q(isPublic=True) | Q(isUnlisted=True))
    
    def get_context_data(self, **kwargs):
        # get duration from seconds
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        context['durationDelta'] = str(datetime.timedelta(seconds=self.object.duration))
        return context

    def get_object(self, queryset=None):
        video = super().get_object(queryset)
        if(not self.request.user.is_authenticated):
            video.views += 1
            video.save()
            return video
        

        video.views += 1
        # check if there's a view with this user and this video, if true, change the date to now
        try:
            view = View.objects.get(viewer=self.request.user,video= video)
            if(view):
                view.date = timezone.now()
                view.save()
        except(KeyError, View.DoesNotExist):
            view = View(viewer= self.request.user, video=video, date=timezone.now())
            view.save()
        video.save()
        return video