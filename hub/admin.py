from django import forms
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


# User
# TODO - Add avatar and banner display to the admin panels for Users
class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class UserAdmin(BaseUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = BaseUserAdmin.fieldsets + (
            ('Custom', {'fields': ('fullname','avatar','banner')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
            ('Custom', {'fields': ('fullname','avatar','banner')}),
    )

# Video
# TODO - Add tags,video, thumbnail and banner display to the admin panels for Videos 
class TagInline(admin.TabularInline):
    model = Tag
    extra = 3

class VideoChangeForm(forms.ModelForm):
    duration = forms.IntegerField(help_text='In seconds')
    quality = forms.CharField(help_text='[width]x[height]')
    class Meta:
        model = Video
        fields = '__all__'

class VideoAdmin(admin.ModelAdmin):
    form = VideoChangeForm
    inlines = [TagInline]
    fieldsets = [
        (None,{'fields': ('title', 'producer','quality','duration','description')}),
        ('Media', {'fields': ('video','thumbnail','banner','storyboard')}),
        ('Date information', {'fields': ('publish_date','lastUpdated',)}),
        ('Privacy', {'fields': ('isPublic','isUnlisted',)}),
    ]
    
# View
class ViewAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,{'fields': ('viewer','video','date')}),
    ]

# Follower 
class FollowerCreationForm(forms.ModelForm):
    class Meta:
        model = Follower
        fields = '__all__'

class FollowerAdmin(admin.ModelAdmin):
    add_form = FollowerCreationForm
    fieldsets = [
        (None,{'fields': ('producer','follower')}),
    ]



# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(Follower,FollowerAdmin)
