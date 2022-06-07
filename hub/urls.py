from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('follow/', views.follow, name='follow'),
    path('unfollow/', views.unfollow, name='unfollow'),
    path('videos/', views.VideosView.as_view(template_name='hub/videos/videos.html'), name='videos'),
    path('video/<int:pk>', views.VideoDetailView.as_view(template_name='hub/videos/video_detail.html'), name='video_detail'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit', views.edit_User, name='edit_user'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='hub/authentication/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]