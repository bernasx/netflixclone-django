from django import forms
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class MyUserChangeForm(UserChangeForm):
    isProducer = forms.BooleanField(help_text='Checks if the user is a producer and has permissions for upload.')

    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):
    isProducer = forms.BooleanField(help_text='Checks if the user is a producer and has permissions for upload.')
    class Meta(UserCreationForm.Meta):
        model = User

class UserAdmin(BaseUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = BaseUserAdmin.fieldsets + (
            ('Custom', {'fields': ('fullname','isProducer')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
            ('Custom', {'fields': ('fullname','isProducer')}),
    )

# Register your models here.
admin.site.register(User, UserAdmin)