from user.forms import RegistrationForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from user.forms import UserRegistrationForm
from user.forms import UserLoginForm, UserUpdateImageForm, UserPostsForm
from user.models import UserImageAlbumsModel, UserPostModel, UserImageModel, Like, Comment


def registration_views(request):
    user_form = ()
    if request.method == "POST":
        print(request.POST)
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()

    context = {"registration_form": user_form}

    return render(request, "registration.html", context)



# Create your views here.


def home(request):
    user_form = userregistration(request)
    form_class = loginuser(request)
    return render(request, 'index.html', {"registration_form": user_form, "login_form": form_class})


def userregistration(request):
    # user_form = ()
    # if request.method == "POST":
    #     print(request.POST)
    user_form = UserRegistrationForm(request.POST)
    if user_form.is_valid():
        user_form.save()
    # context = {"registration_form": user_form}
    return user_form


def loginuser(request):
    form_class = UserLoginForm()
    if request.method == "POST":
        form_class = UserLoginForm(request.POST)
        if form_class.is_valid():
            username = form_class.cleaned_data['username']
            password = form_class.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    return form_class


def user_logout(request):
    logout(request)
    return redirect("home")


@login_required(login_url="loginuser")
def users(request, username):
    user_image = UserImageModel.objects.get(user_id=request.user.id)
    form_image = UserUpdateImageForm()
    if request.method == "POST":
        form_image = UserUpdateImageForm(request.POST, request.FILES, instance=user_image)
        if form_image.is_valid():
            profile_picture = form_image.save(commit=False)
            if request.FILES.get('profile_picture', None) != None:
                profile_picture.profile_picture = request.FILES['profile_picture']
                profile_picture.save()
                UserImageAlbumsModel.objects.create(user_id=request.user.id, status=0,
                                                    profile_picture=request.FILES['profile_picture'])
                return redirect('users', username=request.user.username)
            if request.FILES.get('cover_photo', None) != None:
                profile_picture.cover_photo = request.FILES['cover_photo']
                profile_picture.save()
                UserImageAlbumsModel.objects.create(user_id=request.user.id, status=1,
                                                                 cover_photo=request.FILES['cover_photo'])
                return redirect('users', username=request.user.username)

    return {"user_image": user_image, "form_image": form_image}

@login_required(login_url="loginuser")
def users_posts(request, username):
    post_user = UserPostsForm(request.POST)
    comment_form = CommentForm(request.POST)
    posts_mod = UserPostModel.objects.all()
    contextlike = Like.objects.all()
    comment_all = Comment.objects.all()
    if request.method == "POST":
        post_user = UserPostsForm(request.POST, request.FILES)
        if post_user.is_valid():
            if request.FILES.get('post_picture', None) is not None:
                posts = request.POST['posts']
                status = request.POST['status']
                post_picture = request.FILES['post_picture']
                title = request.POST['title']
                UserPostModel.objects.create(user_id=request.user.id, posts=posts, status=status,
                                             post_picture=post_picture, title=title)
                return redirect('users_posts', username=request.user.username)
            else:
                posts = request.POST['posts']
                status = request.POST['status']
                title = request.POST['title']
                UserPostModel.objects.create(user_id=request.user.id, posts=posts, status=status, title=title)
                return redirect('users_posts', username=request.user.username)

        elif request.POST.get('id', None) is not None:
            like_create_view(request, username)

        elif request.POST.get('comment', None) is not None:
            comment_create_view(request, username)
            return redirect('users_posts', username=request.user.username)
    pages = users(request, username)
    user_image = pages.get('user_image')
    form_image = pages.get('form_image')
    context = {"post": post_user,
               "posts_mod": posts_mod,
               "user_image": user_image,
               "form_image": form_image,
               "contextlike": contextlike,
               "comment_form": comment_form,
               "comment_all": comment_all
               }
    return render(request, 'user/posts.html', context=context)


@login_required(login_url="loginuser")
def users_pos(request, username):
    pages = users(request, username)

    return render(request, 'user/users.html', context=pages)

@login_required(login_url="loginuser")
def like_create_view(request, username):
    if request.method == "POST":
        if request.POST['id']:
            try:
                like = Like.objects.get(user_id=request.user.id, post_user_id=request.POST['id'])
                like.delete()
                update_amout_like = UserPostModel.objects.get(id=request.POST['id'])
                update_amout_like.amount_of_likes -= 1
                update_amout_like.save()

            except:
                Like.objects.create(user_id=request.user.id, post_user_id=request.POST['id'])
                update_amout_like = UserPostModel.objects.get(id=request.POST['id'])
                update_amout_like.amount_of_likes += 1
                update_amout_like.save()

@login_required(login_url="loginuser")
def comment_create_view(request, username):
    if request.method == "POST":
        if request.POST['comment']:
            try:
                Comment.objects.create(user_id=request.user.id, post_user_id=request.POST['post_user_id'],
                                       comment=request.POST['comment'])
            except:
                print('errores')
