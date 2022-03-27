from django.contrib import messages
from django.contrib.auth.models import User
from user.forms import RegistrationForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from user.forms import UserRegistrationForm
from user.forms import UserLoginForm, UserUpdateImageForm, UserPostsForm,CategoryForm
from user.models import UserImageAlbumsModel, UserPostModel, UserImageModel, Like, Comment, Category, Friends


def user_registration(request):
    user_form = UserRegistrationForm()
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "registered successfully")
        else:
            messages.error(request, 'Document deleted.')
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
    posts_mod = UserPostModel.objects.all()
    comment_all = Comment.objects.all()
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
               "comment_form": comment_form,
               "comment_all": comment_all,
               "category": category,
               }
    return render(request, 'user/posts.html', context=context)


def my_posts(request, username):
    post_user = UserPostsForm(request.POST)
    comment_form = CommentForm(request.POST)
    posts_mod = UserPostModel.objects.filter(user=request.user)
    contextlike = Like.objects.filter(user=request.user)
    comment_all = Comment.objects.filter(user=request.user)
    category = CategoryForm(request.POST)
    if request.method == "POST":
        post_user = UserPostsForm(request.POST, request.FILES)
        if post_user.is_valid():
            if request.FILES.get('post_picture', None) is not None:
                posts = request.POST['posts']
                post_picture = request.FILES['post_picture']
                title = request.POST['title']
                UserPostModel.objects.create(user_id=request.user.id, posts=posts,
                                             post_picture=post_picture, title=title)
                return redirect('users_posts', username=request.user.username)
            else:
                posts = request.POST['posts']
                title = request.POST['title']
                UserPostModel.objects.create(user_id=request.user.id, posts=posts, title=title)
                return redirect('users_posts', username=request.user.username)

        elif request.POST.get('like', None) is not None:
            like_create_view(request, username)
        elif request.POST.get('dislike', None) is not None:
            dislike_create_view(request, username)

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
               "comment_all": comment_all,
               "category": category
               }

    return render(request, 'user/posts.html', context=context)


@login_required(login_url="login_user")
def users_pos(request, username):
    pages = users(request, username)

    return render(request, 'user/users.html', context=pages)


@login_required(login_url="login_user")
def like_create_view(request, username):
    if request.method == "POST":
        if request.POST['like']:
            try:
                like = Like.objects.get(user_id=request.user.id, post_user_id=request.POST['like'],like=1)
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
            except:
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
            try:
                Comment.objects.create(user_id=request.user.id, post_user_id=request.POST['post_user_id'],
                                       comment=request.POST['comment'])
            except:
                print('error')


def home(request):
    user_form = user_registration(request)
    form_class = login_user(request)
    return render(request, 'index.html', {"registration_form": user_form, "login_form": form_class})


@login_required(login_url="login_user")
def edit_profile(request, username):
    pages = users(request, username)
    user_form = UserRegistrationForm(instance=request.user)
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, f"task {request.user.username} was update successfully")
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
            return redirect('photos', username=request.user.username)
        elif request.POST.get('cover_photo', None) is not None:
            profile_picture.cover_photo = request.POST['cover_photo']
            profile_picture.save()
            return redirect('photos', username=request.user.username)
        elif request.POST.get('image_id', None) is not None:
            image_album = UserImageAlbumsModel.objects.get(id=request.POST['image_id'])
            image_album.delete()
            return redirect('photos', username=request.user.username)

    context = {"image_album": image_album, **pages}
    return render(request, 'user/photo.html', context=context)


@login_required(login_url="login_user")
def photos_viwes(request, username, id):
    model = UserImageAlbumsModel.objects.get(user__username=username,id=id)
    pages = users(request, username)
    context = {"model": model, **pages}
    return render(request, "user/photo_view.html", context=context)


@login_required(login_url="login_user")
def friend(request, username):
    model = User.objects.exclude(id=request.user.id)
    user_image = UserImageModel.objects.all()
    pages = users(request, username)
    friend_form = Friends.objects.all()
    friend_form_send = Friends.objects.filter(user_id=request.user.id)
    friend_form_received = Friends.objects.filter(friends_id=request.user.id)

    if request.method == "POST":
        if request.POST.get('friends'):
            Friends.objects.get_or_create(user_id=request.user.id, friends_id=request.POST.get('friends'), sent=1)
        if request.POST.get('received'):
           friend = Friends.objects.get(user_id=request.POST.get('received'), friends_id=request.user.id, sent=1)
           friend.received = 1
           friend.save()

    if friend_form_send or friend_form_received:
        context = {
            "model": model,
            "friend_image": user_image,
            "friend_form": friend_form,
            "friend_form_send": friend_form_send,
            **pages
        }

    else:
        context = {
            "model": model,
            "friend_image": user_image,
            **pages
        }
    return render(request, "user/friends.html", context=context)


@login_required(login_url="login_user")
def search(request, username):
    if request.method == "GET":
        if request.GET.get('search', None) is not None:
            users_search = User.objects.filter(username__contains=request.GET["search"])
            if users_search:
                context = {
                    "users_search": users_search,
                }
                return render(request, "user/search.html", context=context)
            else:
                return redirect('home')


# @login_required(login_url="loginuser")
# class SearchResultsView(ListView):
#     model = User
#     template_name = 'user/search.html'

def post_view(request, post_id):

    if UserPostModel.DoesNotExist:
        pass

    post = UserPostModel.objects.get(id=post_id)

    return render(request, "user/post_view.html", {"post_object": post})
