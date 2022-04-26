from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from user.forms import UserRegistrationForm, CommentForm, ProfileForm
from user.forms import UserLoginForm, UserUpdateImageForm, UserPostsForm, CategoryForm
from user.models import UserImageAlbumsModel, UserPostModel, UserImageModel, Like, Comment, Category, Friends, Messages


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
                post_picture = request.FILES['profile_picture']
                posts = "updated his profile picture."
                UserPostModel.objects.create(user_id=request.user.id, posts=posts,
                                             posts_picture=post_picture, share=True)
                UserImageAlbumsModel.objects.create(user_id=request.user.id, status=0,
                                                    profile_picture=request.FILES['profile_picture'])
            if request.FILES.get('cover_photo', None) is not None:
                profile_picture.cover_photo = request.FILES['cover_photo']
                profile_picture.save()
                post_picture = request.FILES['cover_photo']
                posts = "updated his cover photo picture."
                UserPostModel.objects.create(user_id=request.user.id, posts=posts,
                                             posts_picture=post_picture, share=True)
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
                UserPostModel.objects.create(user_id=request.user.id, posts=posts,
                                             posts_picture=post_picture)
                post_id = UserPostModel.objects.all().get(user_id=request.user.id, posts=posts)
                for i in request.POST.getlist('category'):
                    Category.objects.create(category=i, user_id=request.user.id, parent_id=post_id.id)
                messages.success(request, "posts  successfully")
                return redirect('users_posts', username=request.user.username)
            else:
                posts = request.POST['posts']
                UserPostModel.objects.create(user_id=request.user.id, posts=posts)
                post_id = UserPostModel.objects.all().get(user_id=request.user.id, posts=posts)
                for i in request.POST.getlist('category'):
                    Category.objects.create(category=i, user_id=request.user.id, parent_id=post_id.id)
                messages.success(request, "posts  successfully")
                return redirect('users_posts', username=request.user.username)
        elif request.POST.get('share', None) is not None:
            id = request.POST['share']
            post_id = UserPostModel.objects.get(id=id)
            post_id.share = True
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
    posts_mod = UserPostModel.objects.filter(share=True).order_by('-created_at')
    comment_all = Comment.objects.all()
    image_a = UserImageAlbumsModel.objects.filter(user_id=request.user.id)
    image_all = UserImageModel.objects.all()
    category = CategoryForm()
    try:
        image_age = UserImageModel.objects.get(user_id=request.user.id)
        if image_all:
            age = (datetime.now().date() - image_age.birthday) / 365.25
            age = age.days
    except :
        age = ""
    if request.method == "POST":
        post_user = UserPostsForm(request.POST, request.FILES)
        category = CategoryForm(request.POST)

        if post_user.is_valid():
            if request.FILES.get('post_picture', None) is not None:
                posts = request.POST['posts']
                post_picture = request.FILES['post_picture']

                UserPostModel.objects.create(user_id=request.user.id, posts=posts,
                                             posts_picture=post_picture, share=True)
                post_id = UserPostModel.objects.all().get(user_id=request.user.id, posts=posts)
                for i in request.POST.getlist('category'):
                    Category.objects.create(category=i, user_id=request.user.id, parent_id=post_id.id)
                messages.success(request, "posts  successfully")
                return redirect('users_posts', username=request.user.username)
            else:
                posts = request.POST['posts']
                UserPostModel.objects.create(user_id=request.user.id, posts=posts)
                post_id = UserPostModel.objects.all().get(user_id=request.user.id, posts=posts)
                for i in request.POST.getlist('category'):
                    Category.objects.create(category=i, user_id=request.user.id, parent_id=post_id.id)
                messages.success(request, "posts  successfully")
                return redirect('users_posts', username=request.user.username)
        elif request.POST.get('order', None) is not None:
            posts_mod = UserPostModel.objects.filter(share=True).order_by("-"+request.POST.get('order'))
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
    friend = people_all(request, username)
    context = {"post": post_user,
               "posts_mod": posts_mod,
               "user_image": user_image,
               "form_image": form_image,
               "image_all": image_all,
               "image_a": image_a,
               "age": age,
               "comment_form": comment_form,
               "comment_all": comment_all,
               "category": category,
               **friend
               }
    return render(request, 'user/users.html', context=context)


@login_required(login_url="login_user")
def like_create_view(request, username):
    if request.method == "POST":
        if request.POST['like']:
            try:
                like = Like.objects.get(user_id=request.user.id, post_user_id=request.POST['like'], like=True)
                like.delete()
                update_amount_like = UserPostModel.objects.get(id=request.POST['like'])
                update_amount_like.amount_of_likes -= 1
                update_amount_like.save()
            except :
                try:
                    dislike = Like.objects.get(user_id=request.user.id, post_user_id=request.POST['like'], dislike=True)
                    dislike.delete()
                    Like.objects.create(user_id=request.user.id, post_user_id=request.POST['like'], like=True,
                                        dislike=False)
                    update_amount_like = UserPostModel.objects.get(id=request.POST['like'])
                    update_amount_like.amount_of_likes += 1
                    update_amount_like.save()
                    update_amount_dislike = UserPostModel.objects.get(id=request.POST['like'])
                    update_amount_dislike.amount_of_dislikes -= 1
                    update_amount_dislike.save()
                except:
                    Like.objects.create(user_id=request.user.id, post_user_id=request.POST['like'], like=True,
                                        dislike=False)
                    update_amount_like = UserPostModel.objects.get(id=request.POST['like'])
                    update_amount_like.amount_of_likes += 1
                    update_amount_like.save()


@login_required(login_url="login_user")
def dislike_create_view(request, username):
    if request.method == "POST":
        if request.POST['dislike']:
            try:
                dislike = Like.objects.get(user_id=request.user.id, post_user_id=request.POST['dislike'], dislike=True)
                dislike.delete()
                update_amount_dislike = UserPostModel.objects.get(id=request.POST['dislike'])
                update_amount_dislike.amount_of_dislikes -= 1
                update_amount_dislike.save()
            except :
                try:
                    like = Like.objects.get(user_id=request.user.id, post_user_id=request.POST['dislike'], like=True)
                    like.delete()
                    Like.objects.create(user_id=request.user.id, post_user_id=request.POST['dislike'], dislike=True,
                                        like=False)
                    update_amount_like = UserPostModel.objects.get(id=request.POST['dislike'])
                    update_amount_like.amount_of_dislikes += 1
                    update_amount_like.save()
                    update_amount_like = UserPostModel.objects.get(id=request.POST['dislike'])
                    update_amount_like.amount_of_likes -= 1
                    update_amount_like.save()
                except:
                    Like.objects.create(user_id=request.user.id, post_user_id=request.POST['dislike'], dislike=True,
                                        like=False)
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
            pass


def home(request):
    user_form = user_registration(request)
    form_class = login_user(request)
    if request.user.is_authenticated:
        return redirect('users', username=request.user.username)
    return render(request, 'index.html', {"registration_form": user_form, "login_form": form_class})


@login_required(login_url="login_user")
def edit_profile(request, username):

    user_form = ProfileForm(instance=request.user)
    user_image = UserImageModel.objects.get(user_id=request.user.id)
    form_image = UserUpdateImageForm(instance=user_image)
    if request.method == "POST":
        user_form = ProfileForm(request.POST,instance=request.user)
        form_image = UserUpdateImageForm(request.POST, request.FILES, instance=user_image)
        if form_image.is_valid():
            form_image.save()
        if user_form.is_valid():
            user_form.save()
            messages.success(request, f"Profile {request.user.username} was update successfully")
        else:
            messages.error(request, f"Profile {request.user.username} failed to update")
    context = {"user_form": user_form, "user_image": user_image, "form_image": form_image}
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
            post_picture = request.POST['profile_picture']
            posts = "updated his profile picture."
            UserPostModel.objects.create(user_id=request.user.id, posts=posts,
                                         posts_picture=post_picture, share=True)
            messages.success(request, "Profile picture is updated successfully")
            return redirect('photos', username=request.user.username)
        elif request.POST.get('cover_photo', None) is not None:
            profile_picture.cover_photo = request.POST['cover_photo']
            profile_picture.save()
            post_picture = request.POST['cover_photo']
            posts = "updated his cover_photo picture."
            UserPostModel.objects.create(user_id=request.user.id, posts=posts,
                                         posts_picture=post_picture, share=True)

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
    context = people_all(request, username)
    return render(request, "user/friends.html", context=context)


@login_required(login_url="login_user")
def friend_views(request, username, friend_username):
    users_search = search(request, username)
    user_a = User.objects.get(username=friend_username)
    user_imag = UserImageModel.objects.get(user_id=user_a.id)
    image_a = UserImageAlbumsModel.objects.filter(user_id=user_a.id)
    posts_mod = UserPostModel.objects.filter(user_id=user_a.id)
    image_all = UserImageModel.objects.all()
    context = people_all(request, username)
    comment_form = CommentForm(request.POST)
    comment_all = Comment.objects.all()
    return render(request, "user/friends_views.html", context={"user_imag": user_imag, "image_a": image_a,
                                           "user_a": user_a, "posts_mod": posts_mod, "image_all": image_all,
                                            "comment_all": comment_all, "comment_form" :comment_form, **context})


@login_required(login_url="login_user")
def people_all(request, username):
    friend_image = UserImageModel.objects.all()
    friend_f = Friends.objects.filter(user_from_id=request.user.id).values_list('user_to_id')
    friend_for = Friends.objects.all().filter(user_to_id=request.user.id).values_list('user_from_id')
    friend_form = Friends.objects.all()
    model_s = User.objects.exclude(id=request.user.id)
    model_a = model_s.exclude(id__in=friend_f)
    model = model_a.exclude(id__in=friend_for)
    pages = users(request, username)
    if request.method == "POST":
        if request.POST.get('send'):
            Friends.objects.get_or_create(user_from_id=request.user.id, user_to_id=request.POST.get('send'), send=True)
        elif request.POST.get('accept'):
            received = Friends.objects.get(user_from_id=request.POST.get('accept'), user_to_id=request.user.id, send=True)
            received.accept = True
            received.save()
    if request.method == "GET":
        if request.GET.get('search', None) is not None:
            users_search = model.filter(username__contains=request.GET["search"]).values_list('id')
            friend_form = friend_form.filter(user_to_id=users_search)
            print(users_search)
            print(friend_form)
            print("friend_form")
            if users_search:

                context = {
                    "model": users_search,
                    "friend_image": friend_image,
                    "friend_form": friend_form,
                    **pages
                }
                return render(request, "user/search.html", context=context)
            else:
                return redirect('search')

    context = {
        "model": model,
        "friend_form": friend_form,
        "friend_image": friend_image,
        **pages
    }
    return context


@login_required(login_url="login_user")
def people(request, username):
    context = people_all(request, username)
    return render(request, "user/people.html", context=context)


@login_required(login_url="login_user")
def people_view(request, user_id):
    model = User.objects.get(id=user_id)
    image_album_all = UserImageAlbumsModel.objects.filter(user_id=user_id)
    date = datetime.now()
    # print(date)
    # print()
    # date = (datetime.now() > model.last_login.time)
    pages = users(request, model.username)

    try:
        image_all = UserImageModel.objects.get(user_id=user_id)
        if image_all:
            age = (datetime.now().date() - image_all.birthday) / 365.25
            age = age.days
    except:
        age = ""

    context = {
        "model": model,
        "age": age,
        "date": date,
        "image_all": image_all,
        "image_album_all": image_album_all,
        **pages
    }
    return render(request, "user/friends_views.html", context=context)


@login_required(login_url="login_user")
def search(request, username):
    # pages = users(request, username)
    user_image = UserImageModel.objects.all()
    if request.method == "GET":
        if request.GET.get('search', None) is not None:
            users_search = User.objects.filter(username__icontains=request.GET["search"], first_name__icontains=request.GET["search"])
            if users_search:
                context = {
                    "model": users_search,
                    "friend_image": user_image,
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


def messages_sed(request, username, id):
    user_all = User.objects.get(id=id)
    image_to = UserImageModel.objects.get(user_id=id)
    image_from = UserImageModel.objects.get(user_id=request.user.id)
    messages_all = Messages.objects.all()
    if request.method == "POST":
        if request.POST['messages_from']:
            Messages.objects.create(user_from_id=request.user.id, messages_from=request.POST['messages_from'],
                                     user_to_id=id)

    return render(request, "user/messages.html", context={"messages_all": messages_all, "user_all": user_all,
                                                          "image_to": image_to, "image_from": image_from})