from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from user.models import UserImageModel, Comment


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password1'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password2'}))

    def validate(self, value):
        data = self.get_initial()
        username = data.get("username")
        email = data.get("email")
        password1 = data.get("password1")
        password2 = data.get("password2")
        max_similarity = 0.7
        user_qs = User.objects.filter(username=username)
        if user_qs.exists():
            raise ValidationError("Username already exist")
            if (password1 != password2):
                raise ValidationError("Password and Confirm password does not match")
                print("Password and Confirm password does not match")
                messages.error("Password and Confirm password does not match")
        if SequenceMatcher(a=password.lower(), b=username.lower()).quick_ratio() > max_similarity:
            raise serializers.ValidationError("The password is too similar to the username.")
            messages.error("The password is too similar to the username.")
        if SequenceMatcher(a=password.lower(), b=email.lower()).quick_ratio() > max_similarity:
            raise serializers.ValidationError("The password is too similar to the email.")
            messages.error("The password is too similar to the email.")
        return data





    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


# class UserCommentForm(forms.ModelForm):
#     comment = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}), required=False)
#
#     class Meta:
#         model = UserCommentModel
#         fields = ('comment',)


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


class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows": "1",
                                                           "placeholder": "Comment"}), required=False)

    class Meta:
        model = Comment
        fields = ('comment',)


# class likeModelForm(forms.ModelForm):
#     like = forms.TextInput(widget=forms.TextInput(attrs={"class": "form-control", "rows": "1",
#                                                            "placeholder": "Comment"}), required=False)
#
#     class Meta:
#         model = Comment
#         fields = ('comment',)