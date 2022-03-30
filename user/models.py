from django.contrib.auth.models import User, AbstractUser
from django.db import models


def user_image_directory_path(instance, filename):
    return 'profile/images/{0}/{1}'.format(instance.id, filename)


class UserImageModel(models.Model):
    STATUS_CHOICE = (
        (0, "female"),
        (1, "male"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    birthday = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(default='/a1.jpg', upload_to=user_image_directory_path, blank=True, null=True)
    cover_photo = models.ImageField(default='/cover_photo.jpg', upload_to=user_image_directory_path, blank=True,
                                    null=True)
    photo_albums = models.ImageField(upload_to=user_image_directory_path, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    location = models.TextField(max_length=100, blank=True, null=True)
    gender = models.IntegerField(choices=STATUS_CHOICE, blank=True, null=True,default=0)

    def __str__(self):
        return self.created_at


class UserImageAlbumsModel(models.Model):
    STATUS_CHOICE = (
        (0, "PROFILE"),
        (1, "COVER"),
        (2, "ALBUMS"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICE)
    profile_picture = models.ImageField(default='/a1.jpg', upload_to=user_image_directory_path)

    def __str__(self):
        return self.created_at


def user_post_directory_path(instance, filename):
    return 'profile/images/post/{0}/{1}'.format(instance.id, filename)


class Category(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey("UserPostModel", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices=CATHEGORIES, blank=True, null=True, max_length=10)

    def __str__(self):
        return self.category


class UserPostModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    posts_picture = models.ImageField(upload_to=user_post_directory_path)
    posts = models.TextField()
    share = models.BooleanField(default=False)
    amount_of_likes = models.IntegerField(default=0)
    amount_of_dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.posts

    class Meta:
        ordering = ['-created_at']


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_user = models.ForeignKey(UserPostModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)

    def __str__(self):
        return self.like, self.dislike


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_user = models.ForeignKey(UserPostModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return self.comment


class Friends(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_to')
    accept = models.BooleanField(default=False, blank=True, null=True)
    send = models.BooleanField(default=False,  blank=True, null=True)


class Messages(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_messages_to')
    messages_from = models.TextField(blank=True, null=True)
    messages_to = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


