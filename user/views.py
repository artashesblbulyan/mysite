from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from user.forms import UserRegistrationForm, CommentForm
from user.forms import UserLoginForm, UserUpdateImageForm, UserPostsForm,CategoryForm
from user.models import UserImageAlbumsModel, UserPostModel, UserImageModel, Like, Comment, Category, Friends


def user_registration(request):
    user_form = UserRegistrationForm()
    if request.method == "POST":
        if request.POST.get('register-submit', None) is not None:
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "registered successfully")
            else:
                messages.error(request, 'Registration failed')
    return user_form


def login_user(request):
    form_class = UserLoginForm()
    if request.method == "POST":
        form_class = UserLoginForm(request.POST)
        if form_class.is_valid():
            username = form_class.cleaned_data['username']
            password = form_class.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "logged in successfully")
                return redirect('home')
            else:
                messages.error(request, "invalid username or password")
    return form_class


@login_required(login_url="login_user")
def user_logout(request):
    logout(request)
    return redirect("home")


@login_required(login_url="login_user")
def users(request, username):
    users_search = search(request, username)
    user_image = UserImageModel.objects.get(user_id=request.user.id)
    form_image = UserUpdateImageForm()
    if request.method == "POST":
        form_image = UserUpdateImageForm(request.POST, request.FILES, instance=user_image)
        if form_image.is_valid():
            profile_picture = form_image.save(commit=False)
            if request.FILES.get('profile_picture', None) is not None:
                profile_picture.profile_picture = request.FILES['profile_picture']
                profile_picture.save()
                UserImageAlbumsModel.objects.create(user_id=request.user.id, status=0,
                                                    profile_picture=request.FILES['profile_picture'])
            elif request.FILES.get('cover_photo', None) is not None:
                profile_picture.cover_photo = request.FILES['cover_photo']
                profile_picture.save()
                UserImageAlbumsModel.objects.create(user_id=request.user.id, status=1,
                                                    profile_picture=request.FILES['cover_photo'])
    return {"user_image": user_image, "form_image": form_image}


@login_required(login_url="login_user")
def users_posts_create(request, username):
    post_user = UserPostsForm(request.POST)
    comment_form = CommentForm(request.POST)
    posts_mod = UserPostModel.objects.filter(user=request.user)
    comment_all = Comment.objects.all()
    image_all = UserImageModel.objects.all()
    category = CategoryForm()
    if request.method == "POST":
        post_user = UserPostsForm(request.POST, request.FILES)
        category = CategoryForm(request.POST)
        if post_user.is_valid():
            if request.FILES.get('post_picture', None) is not None:
                posts = request.POST['posts']
                post_picture = request.FILES['post_picture']
                title = request.POST['title']
                UserPostModel.objects.create(user_id=request.user.id, posts=posts,
                                             posts_picture=post_picture, title=title)
                post_id = UserPostModel.objects.all().get(user_id=request.user.id, posts=posts, title=title)
                for i in request.POST.getlist('category'):
                    Category.objects.create(category=i, user_id=request.user.id, parent_id=post_id.id)
                messages.success(request, "posts  successfully")
                return redirect('users_posts', username=request.user.username)
            else:
                posts = request.POST['posts']
                title = request.POST['title']
                UserPostModel.objects.create(user_id=request.user.id, posts=posts,  title=title)
                post_id = UserPostModel.objects.all().get(user_id=request.user.id, posts=posts, title=title)
                for i in request.POST.getlist('category'):
                    Category.objects.create(category=i, user_id=request.user.id, parent_id=post_id.id)
                messages.success(request, "posts  successfully")
                return redirect('users_posts', username=request.user.username)
        elif request.POST.get('share', None) is not None:
            id = request.POST['share']
            post_id = UserPostModel.objects.get(id=id)
            post_id.share = 1
            post_id.save()
        elif request.POST.get('like', None) is not None:
            like_create_view(request, username)
        elif request.POST.get('dislike', None) is not None:
            dislike_create_view(request, username)
        elif request.POST.get('comment', None) is not None:
            comment_create_view(request, username)
            return redirect('users_posts', username=request.user.username)
    if request.method == "GET":
        if request.GET.get('category', None) is not None:
            queryset = Category.objects.all()
            queryset = queryset.filter(category=request.GET.get('category'))
            queryset = queryset.values_list('parent_id', flat=True).order_by('category')
            posts_mod = []
            for i in queryset:
                posts_mod += UserPostModel.objects.filter(id=i)
    pages = users(request, username)
    user_image = pages.get('user_image')
    form_image = pages.get('form_image')
    context = {"post": post_user,
               "posts_mod": posts_mod,
               "user_image": user_image,
               "form_image": form_image,
               "image_all": image_all,
               "comment_form": comment_form,
               "comment_all": comment_all,
               "category": category,
               }
    return render(request, 'user/posts.html', context=context)


@login_required(login_url="login_user")
def users_pos(request, username):
    post_user = UserPostsForm(request.POST)
    comment_form = CommentForm(request.POST)
    posts_mod = UserPostModel.objects.filter(share=1).order_by('-created_at')
    comment_all = Comment.objects.all()
    image_all = UserImageModel.objects.all()
    category = CategoryForm()
    if request.method == "POST":
        post_user = UserPostsForm(request.POST, request.FILES)
        category = CategoryForm(request.POST)
        if post_user.is_valid():
            if request.FILES.get('post_picture', None) is not None:
                posts = request.POST['posts']
                post_picture = request.FILES['post_picture']
                title = request.POST['title']
                UserPostModel.objects.create(user_id=request.user.id, posts=posts,
                                             posts_picture=post_picture, title=title, share=1)
                post_id = UserPostModel.objects.all().get(user_id=request.user.id, posts=posts, title=title)
                for i in request.POST.getlist('category'):
                    Category.objects.create(category=i, user_id=request.user.id, parent_id=post_id.id)
                messages.success(request, "posts  successfully")
                return redirect('users_posts', username=request.user.username)
            else:
                posts = request.POST['posts']
                title = request.POST['title']
                UserPostModel.objects.create(user_id=request.user.id, posts=posts, title=title)
                post_id = UserPostModel.objects.all().get(user_id=request.user.id, posts=posts, title=title)
                for i in request.POST.getlist('category'):
                    Category.objects.create(category=i, user_id=request.user.id, parent_id=post_id.id)
                messages.success(request, "posts  successfully")
                return redirect('users_posts', username=request.user.username)
        elif request.POST.get('order', None) is not None:
            posts_mod = UserPostModel.objects.filter(share=1).order_by("-"+request.POST.get('order'))
        elif request.POST.get('like', None) is not None:
            like_create_view(request, username)
        elif request.POST.get('dislike', None) is not None:
            dislike_create_view(request, username)
        elif request.POST.get('comment', None) is not None:
            comment_create_view(request, username)
            return redirect('users', username=request.user.username)
    if request.method == "GET":
        if request.GET.get('category', None) is not None:
            queryset = Category.objects.all()
            queryset = queryset.filter(category=request.GET.get('category'))
            queryset = queryset.values_list('parent_id', flat=True).order_by('category')
            posts_mod = []
            for i in queryset:
                posts_mod += UserPostModel.objects.filter(id=i)
    pages = users(request, username)
    user_image = pages.get('user_image')
    form_image = pages.get('form_image')
    context = {"post": post_user,
               "posts_mod": posts_mod,
               "user_image": user_image,
               "form_image": form_image,
               "image_all": image_all,
               "comment_form": comment_form,
               "comment_all": comment_all,
               "category": category,
               }
    return render(request, 'user/users.html', context=context)


@login_required(login_url="login_user")
def like_create_view(request, username):
    if request.method == "POST":
        if request.POST['like']:
            try:
                like = Like.objects.get(user_id=request.user.id, post_user_id=request.POST['like'], like=1)
                like.delete()
                update_amount_like = UserPostModel.objects.get(id=request.POST['like'])
                update_amount_like.amount_of_likes -= 1
                update_amount_like.save()
            except:
                try:
                    dislike = Like.objects.get(user_id=request.user.id, post_user_id=request.POST['like'], dislike=1)
                    dislike.delete()
                    Like.objects.create(user_id=request.user.id, post_user_id=request.POST['like'],like=1,dislike=0)
                    update_amount_like = UserPostModel.objects.get(id=request.POST['like'])
                    update_amount_like.amount_of_likes += 1
                    update_amount_like.save()
                    update_amount_dislike = UserPostModel.objects.get(id=request.POST['like'])
                    update_amount_dislike.amount_of_dislikes -= 1
                    update_amount_dislike.save()
                except:
                    Like.objects.create(user_id=request.user.id, post_user_id=request.POST['like'], like=1,dislike=0 )
                    update_amount_like = UserPostModel.objects.get(id=request.POST['like'])
                    update_amount_like.amount_of_likes += 1
                    update_amount_like.save()


@login_required(login_url="login_user")
def dislike_create_view(request, username):
    if request.method == "POST":
        if request.POST['dislike']:
            try:
                dislike = Like.objects.get(user_id=request.user.id, post_user_id=request.POST['dislike'], dislike=1)
                dislike.delete()
                update_amount_dislike = UserPostModel.objects.get(id=request.POST['dislike'])
                update_amount_dislike.amount_of_dislikes -= 1
                update_amount_dislike.save()
            except :
                try:
                    like = Like.objects.get(user_id=request.user.id, post_user_id=request.POST['dislike'], like=1)
                    like.delete()
                    Like.objects.create(user_id=request.user.id, post_user_id=request.POST['dislike'], dislike=1, like=0)
                    update_amount_like = UserPostModel.objects.get(id=request.POST['dislike'])
                    update_amount_like.amount_of_dislikes += 1
                    update_amount_like.save()
                    update_amount_like = UserPostModel.objects.get(id=request.POST['dislike'])
                    update_amount_like.amount_of_likes -= 1
                    update_amount_like.save()
                except:
                    Like.objects.create(user_id=request.user.id, post_user_id=request.POST['dislike'], dislike=1, like=0)
                    update_amount_like = UserPostModel.objects.get(id=request.POST['dislike'])
                    update_amount_like.amount_of_dislikes += 1
                    update_amount_like.save()


@login_required(login_url="login_user")
def comment_create_view(request, username):
    if request.method == "POST":
        if request.POST['comment']:
            Comment.objects.create(user_id=request.user.id, post_user_id=request.POST['post_user_id'],
                                   comment=request.POST['comment'])
        else:
            return redirect('users_posts', username=request.user.username)


def home(request):
    user_form = user_registration(request)
    form_class = login_user(request)
    if request.user.is_authenticated:
        return redirect('users', username=request.user.username)
    return render(request, 'index.html', {"registration_form": user_form, "login_form": form_class})


@login_required(login_url="login_user")
def edit_profile(request, username):
    pages = users(request, username)
    user_form = UserRegistrationForm(instance=request.user)
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, f"Profile {request.user.username} was update successfully")
        else:
            messages.error(request, f"Profile {request.user.username} failed to update")
    context = {"user_form": user_form, **pages}
    return render(request, 'user/edit_profile.html', context=context)


@login_required(login_url="login_user")
def photos(request, username):
    pages = users(request, username)
    image_album = UserImageAlbumsModel.objects.filter(user_id=request.user.id)
    if request.method == "POST":
        profile_picture = UserImageModel.objects.get(user_id=request.user.id)
        if request.POST.get('profile_picture', None) is not None:
            profile_picture.profile_picture = request.POST['profile_picture']
            profile_picture.save()
            messages.success(request, "Profile picture is updated successfully")
            return redirect('photos', username=request.user.username)
        elif request.POST.get('cover_photo', None) is not None:
            profile_picture.cover_photo = request.POST['cover_photo']
            profile_picture.save()
            messages.success(request, "Cover photo is updated successfully")
            return redirect('photos', username=request.user.username)
        elif request.POST.get('image_id', None) is not None:
            image_album = UserImageAlbumsModel.objects.get(id=request.POST['image_id'])
            image_album.delete()
            return redirect('photos', username=request.user.username)

    context = {"image_album": image_album, **pages}
    return render(request, 'user/photo.html', context=context)


@login_required(login_url="login_user")
def photos_viwes(request, username, id):
    model = UserImageAlbumsModel.objects.get(user__username=username, id=id)
    pages = users(request, username)
    context = {"model": model, **pages}
    return render(request, "user/photo_view.html", context=context)


@login_required(login_url="login_user")
def friend(request, username):

    user_image = UserImageModel.objects.all()
    pages = users(request, username)
    friend_form = Friends.objects.all().filter(user_id=request.user.id, sent=1, received=1)
    friend_form_1 = Friends.objects.all().filter(friends_id=request.user.id, sent=1, received=1)

    model = User.objects.exclude(id=request.user.id)
    # if request.method == "POST":
    #     if request.POST.get('friends'):
    #         Friends.objects.get_or_create(user_id=request.user.id, friends_id=request.POST.get('friends'), sent=1)
    #     elif request.POST.get('received'):
    #         received = Friends.objects.get(user_id=request.POST.get('received'), friends_id=request.user.id, sent=1)
    #         received.received = 1
    #         received.save()
    # if friend_form_send or friend_form_received:
    context = {
        "model": model,
        "friend_image": user_image,
        "friend_form": friend_form,
        "friend_form_1": friend_form_1,

        **pages
    }
    # else:
    #     context = {
    #         "model": model,
    #         "friend_image": user_image,
    #         **pages
    #     }
    return render(request, "user/friends.html", context=context)


@login_required(login_url="login_user")
def people(request, username):
    model = User.objects.exclude(id=request.user.id)
    user_image = UserImageModel.objects.all()
    friend_form = Friends.objects.all().filter(user_id=request.user.id, sent=1, received=1)
    friend_form_3 = Friends.objects.all().filter(user_id=request.user.id, sent=1, received=0)
    friend_form_1 = Friends.objects.all().filter(friends_id=request.user.id, sent=1, received=1)
    friend_form_2 = Friends.objects.all().filter(friends_id=request.user.id, sent=1, received=0)
    pages = users(request, username)
    if request.method == "POST":
        if request.POST.get('friends'):
            Friends.objects.get_or_create(user_id=request.user.id, friends_id=request.POST.get('friends'), sent=1)
        elif request.POST.get('received'):
            received = Friends.objects.get(user_id=request.POST.get('received'), friends_id=request.user.id, sent=1)
            received.received = 1
            received.save()

    context = {
        "model": model,
        "friend_image": user_image,
        "friend_form": friend_form,
        "friend_form_1": friend_form_1,
        "friend_form_2": friend_form_2,
        "friend_form_3": friend_form_3,
        **pages
    }

    return render(request, "user/People.html", context=context)

@login_required(login_url="login_user")
def search(request, username):
    # pages = users(request, username)
    if request.method == "GET":
        if request.GET.get('search', None) is not None:
            users_search = User.objects.filter(username__contains=request.GET["search"])
            if users_search:
                context = {
                    "users_search": users_search,
                    # **pages
                }
                return render(request, "user/search.html", context=context)
            else:
                return redirect('search')


@login_required(login_url="login_user")
def post_view(request, username, post_id):
    if request.method == "POST":
        if request.POST.get('comment_delete'):
            comment_all = Comment.objects.get(id=request.POST.get('comment_delete'))
            comment_all.delete()
        if request.POST.get('post_delete'):
            comment_all = UserPostModel.objects.get(user__username=username, id=request.POST.get('post_delete'))
            comment_all.delete()
            return redirect('users_posts', username=request.user.username)
    post = UserPostModel.objects.get(user__username=username, id=post_id)
    pages = users(request, username)
    comment_all = Comment.objects.filter(post_user_id=post_id)
    context = {
        "comment_all": comment_all,
        "post_object": post,
        **pages
    }
    return render(request, "user/post_view.html", context=context)

