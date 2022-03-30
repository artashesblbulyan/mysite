from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from user.models import UserImageModel, Comment


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Name', "class":"form-control","tabindex":"1"}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', "class":"form-control","tabindex":"1"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', "class":"form-control","tabindex":"1"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Email Address","tabindex":"1"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', "class":"form-control","tabindex":"2"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', "class":"form-control","tabindex":"2"}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


# class UserCommentForm(forms.ModelForm):
#     comment = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}), required=False)
#
#     class Meta:
#         model = UserCommentModel
#         fields = ('comment',)


# class RegistrationForm(UserCreationForm):
#     first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
#     email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
#
#     def validate(self, value):
#         data = self.get_initial()
#         username = data.get("username")
#         email = data.get("email")
#         password1 = data.get("password1")
#         password2 = data.get("password2")
#         max_similarity = 0.7
#         user_qs = User.objects.filter(username=username)
#         if user_qs.exists():
#             raise ValidationError("Username already exist")
#             if (password1 != password2):
#                 raise ValidationError("Password and Confirm password does not match")
#                 print("Password and Confirm password does not match")
#                 messages.error("Password and Confirm password does not match")
#         if SequenceMatcher(a=password.lower(), b=username.lower()).quick_ratio() > max_similarity:
#             raise serializers.ValidationError("The password is too similar to the username.")
#             messages.error("The password is too similar to the username.")
#         if SequenceMatcher(a=password.lower(), b=email.lower()).quick_ratio() > max_similarity:
#             raise serializers.ValidationError("The password is too similar to the email.")
#             messages.error("The password is too similar to the email.")
#         return data
#
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', "class":"form-control","tabindex":"1"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', "class":"form-control","tabindex":"2"}))


class UserUpdateImageForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    cover_photo = forms.ImageField(required=False)
    photo_albums = forms.ImageField(required=False)

    class Meta:
        model = UserImageModel
        fields = ("profile_picture", "cover_photo", "photo_albums")


class UserPostsForm(forms.Form):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Title',
                                                                          "class": "post_input titel"}))
    posts = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description', "class": "post_input posts"}))
    post_picture = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'placeholder': 'Description'}))


class CategoryForm(forms.Form):
    CATHEGORIES = (
        (0, "Communication"),
        (1, "Conference Report"),
        (2, "Editorial"),
        (3, "Opinion"),
        (4, "Perspective"),
        (5, "Book Review"),
        (6, "Registered Report"),
        (7, "Review"),
        (8, "Else"),
    )

    category = forms.ChoiceField(choices=CATHEGORIES, required=True,
                                 widget=forms.Select(attrs={"multiple": "multiple",
                                                            "size": "3", "class": "form-category-posts"}))


class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows": "1",
                                                           "placeholder": "Comment"}), required=False)

    class Meta:
        model = Comment
        fields = ('comment',)


# class FrendForm(forms.ModelForm):
#     like = forms.TextInput(widget=forms.TextInput(attrs={"class": "form-control", "rows": "1",
#                                                            "placeholder": "Comment"}), required=False)
#     frends = forms.IntegerField(widget=forms.Submit(attrs={"class": "form-control", "rows": "1",
#                                                            "placeholder": "Comment"}), required=False)
#     received = forms.IntegerField(default=0, blank=True, null=True)
#     sent = forms.IntegerField(default=0, blank=True, null=True)
#     class Meta:
#         model = Comment
#         fields = ('comment',)