from django import forms
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Movie


# User
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
            ('Custom', {'fields': ('fullname',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
            ('Custom', {'fields': ('fullname',)}),
    )

# Movie
class MovieChangeForm(forms.ModelForm):
    duration = forms.IntegerField(help_text='In seconds')
    quality = forms.CharField(help_text='[width]x[height]')
    class Meta:
        model = Movie
        fields = '__all__'

class MovieAdmin(admin.ModelAdmin):
    form = MovieChangeForm
    fieldsets = [
        (None,{'fields': ('title', 'producer','quality','duration','description')}),
        ('Date information', {'fields': ('publish_date','lastUpdated',)}),
        ('Privacy', {'fields': ('isPublic','isUnlisted',)}),
    ]
    


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Movie, MovieAdmin)