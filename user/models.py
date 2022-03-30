from django.contrib.auth.models import User
from django.db import models


def user_image_directory_path(instance, filename):
    return 'profile/images/{0}/{1}'.format(instance.id, filename)


class UserImageModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(default='/a1.jpg', upload_to=user_image_directory_path, blank=True, null=True)
    cover_photo = models.ImageField(default='/cover_photo.jpg', upload_to=user_image_directory_path, blank=True,
                                    null=True)
    photo_albums = models.ImageField(upload_to=user_image_directory_path, blank=True, null=True)

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
    title = models.CharField(max_length=200)
    share = models.IntegerField(default=0)
    amount_of_likes = models.IntegerField(default=0)
    amount_of_dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_user = models.ForeignKey(UserPostModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=1)
    dislike = models.IntegerField(default=1)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friends_id = models.IntegerField(default=0)
    received = models.IntegerField(default=0, blank=True, null=True)
    sent = models.IntegerField(default=0,  blank=True, null=True)
