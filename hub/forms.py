from django import forms

class UserEditForm(forms.Form):
    avatar = forms.ImageField()
    banner = forms.ImageField()