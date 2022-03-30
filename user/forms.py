from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from user.models import UserImageModel, Comment


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Name', "class": "form-control",
                                                               "tabindex": "1"}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', "class": "form-control",
                                                             "tabindex": "1"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', "class": "form-control",
                                                              "tabindex": "1"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email Address",
                                                           "tabindex": "1"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', "class": "form-control",
                                                                  "tabindex": "2"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', "class": "form-control",
                                                                  "tabindex": "2"}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', "class": "form-control"}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Your Name', "class": "form-control"}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', "class": "form-control"}),
            'email': forms.TextInput(attrs={"class": "form-control", "placeholder": "Email Address"}),
                }


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', "class": "form-control",
                                                             "tabindex": "1"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', "class": "form-control",
                                                                 "tabindex": "2"}))


class UserUpdateImageForm(forms.ModelForm):
    STATUS_CHOICE = (
        (0, "female"),
        (1, "male"),
    )
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={
                                                             "class": "btn btn-primary"}))
    cover_photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={
                                                             "class": "btn btn-primary"}))
    photo_albums = forms.ImageField(required=False)
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': '02/02/2022',
                                                             "class": "form-control"}), required=False)
    phone_number = forms.CharField(max_length=12, required=False, widget=forms.NumberInput(attrs={"type": "tel",
                                                         'placeholder': '+374 93 012345', "class": "form-control"}))
    location = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
                                                             'placeholder': 'Location', "class": "form-control"}))
    gender = forms.ChoiceField(choices=STATUS_CHOICE, required=False, widget=forms.Select(attrs={'placeholder':
                                                                 'gender', "class": "form-control", "value": 0}))

    class Meta:
        model = UserImageModel
        fields = ("profile_picture", "cover_photo", "photo_albums", "birthday", "location", "gender","phone_number")


class UserPostsForm(forms.Form):
    posts = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description',"rows":"2",
                                                         "class": "form-control input-lg p-text-area"}))
    post_picture = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'placeholder': 'Description',
                                  "class": "btn btn-default dropdown-toggle waves-effect" }))


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
                                 widget=forms.Select(attrs={"class": "btn btn-default btn-circle",
                                                "data-toggle": "dropdown"}))


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