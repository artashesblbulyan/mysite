from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View, TemplateView
from user.forms import RegistrationForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from user.forms import UserRegistrationForm
from user.forms import UserLoginForm, UserUpdateImageForm, UserPostsForm
from user.models import UserImageAlbumsModel, UserPostModel, UserImageModel, Like, Comment, Category



def registration_views(request):
    user_form = ()
    if request.method == "POST":
        print(request.POST)
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success("you are registered successfully")

    context = {"registration_form": user_form}

    return render(request, "registration.html", context)


def userregistration(request):
    # user_form = ()
    # if request.method == "POST":
    #     print(request.POST)
    user_form = UserRegistrationForm(request.POST)
    if user_form.is_valid():
        user_form.save()
        messages.success(request, "registered successfully")
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
                messages.success(request, "logged in successfully")
                return redirect('home')
            else:
                messages.error(request, "invalid username or password")
    return form_class


def home(request):
    user_form = userregistration(request)
    form_class = loginuser(request)
    return render(request, 'index.html', {"registration_form": user_form, "login_form": form_class})


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
            if request.FILES.get('profile_picture', None) is not None:
                profile_picture.profile_picture = request.FILES['profile_picture']
                profile_picture.save()
                UserImageAlbumsModel.objects.create(user_id=request.user.id, status=0,
                                                    profile_picture=request.FILES['profile_picture'])
                return redirect('users', username=request.user.username)
            if request.FILES.get('cover_photo', None) is not None:
                profile_picture.cover_photo = request.FILES['cover_photo']
                profile_picture.save()
                UserImageAlbumsModel.objects.create(user_id=request.user.id, status=1,
                                                                 profile_picture=request.FILES['cover_photo'])
                return redirect('users', username=request.user.username)

    return {"user_image": user_image, "form_image": form_image}


@login_required(login_url="loginuser")
def users_posts(request, username):
    post_user = UserPostsForm(request.POST)
    comment_form = CommentForm(request.POST)
    posts_mod = UserPostModel.objects.all()
    contextlike = Like.objects.all()
    comment_all = Comment.objects.all()
    cathegory = Category.objects.all()
    if request.method == "POST":
        post_user = UserPostsForm(request.POST, request.FILES)
        if post_user.is_valid():
            if request.FILES.get('post_picture', None) is not None:
                posts = request.POST['posts']
                status = request.POST['status']
                post_picture = request.FILES['post_picture']
                title = request.POST['title']
                cath = request.POST['cathegory']
                UserPostModel.objects.create(user_id=request.user.id, posts=posts, status=status,
                                             post_picture=post_picture, title=title)
                return redirect('users_posts', username=request.user.username)
            else:
                posts = request.POST['posts']
                status = request.POST['status']
                title = request.POST['title']
                cath = request.POST['cathegory']
                UserPostModel.objects.create(user_id=request.user.id, posts=posts, status=status, title=title)
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
               "comment_all": comment_all
               }
    return render(request, 'user/posts.html', context=context)


def my_posts(request, username):
    post_user = UserPostsForm(request.POST)
    comment_form = CommentForm(request.POST)
    posts_mod = UserPostModel.objects.filter(user=request.user)
    contextlike = Like.objects.filter(user=request.user)
    comment_all = Comment.objects.filter(user=request.user)
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
               "comment_all": comment_all
               }

    return render(request, 'user/posts.html', context=context)


@login_required(login_url="loginuser")
def users_pos(request, username):
    pages = users(request, username)

    return render(request, 'user/users.html', context=pages)


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



def comment_create_view(request, username):
    if request.method == "POST":
        print('error1')
        if request.POST['comment']:
            try:
                Comment.objects.create(user_id=request.user.id, post_user_id=request.POST['post_user_id'],
                                       comment=request.POST['comment'])
            except:
                print('error')





@login_required(login_url="loginuser")
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

#
@login_required(login_url="loginuser")
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


# class Photos(LoginRequiredMixin, ListView):
#     model = UserImageAlbumsModel
#     ordering = "-date"
#     template_name = "user/photo.html"
#     success_url = 'photos'
#
#     def get_context_data(self, **kwargs):
#         context = super(Photos, self).get_context_data(**kwargs)
#         pages = users(self.request, self.request.user.username)
#         context["user_image"] = pages.get('user_image')
#         context["form_image"] = pages.get('form_image')
#         return context
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)
#
#     def post(self, request, **kwargs):
#         pages = users(self.request, self.request.user.username)
#         messages.success(request, "create")
#         return redirect("home")

@login_required(login_url="loginuser")
def photos_viwes(request, username, id):
    model = UserImageAlbumsModel.objects.get(user__username=username,id=id)
    pages = users(request, username)
    context = {"model": model, **pages}
    return render(request, "user/photo_view.html", context=context)
