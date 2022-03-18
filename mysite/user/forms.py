from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from user_admin.models import UserImageModel


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class UserUpdateImageForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    cover_photo = forms.ImageField(required=False)
    photo_albums = forms.ImageField(required=False)

    class Meta:
        model = UserImageModel
        fields = ("profile_picture", "cover_photo", "photo_albums")


class UserPostsForm(forms.Form):
    STATUS_CHOICE = (
        (0, "COMPLETE"),
        (1, "RUNNING"),
        (2, "UPCOMING"),
    )
    title = forms.CharField(max_length=200)
    posts = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Posts'}))
    status = forms.ChoiceField(choices=STATUS_CHOICE, required=True)
    post_picture = forms.ImageField(required=False)


