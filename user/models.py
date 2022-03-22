from django.contrib.auth.models import User
from django.db import models


# class UserCommentModel(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now_add=True)
#     comment = models.TextField()
#
#     def __str__(self):
#         return self.comment


def user_image_directory_path(instance, filename):
    return 'profile/images/{0}/{1}'.format(instance.id, filename)


class UserImageModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(default='/a1.jpg', upload_to=user_image_directory_path)
    cover_photo = models.ImageField(upload_to=user_image_directory_path)
    photo_albums = models.ImageField(upload_to=user_image_directory_path)

    def __str__(self):
        return self.date


class UserImageAlbumsModel(models.Model):
    STATUS_CHOICE = (
        (0, "PROFILE"),
        (1, "COVER"),
        (2, "ALBUMS"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICE)
    profile_picture = models.ImageField(default='/a1.jpg', upload_to=user_image_directory_path)

    def __str__(self):
        return self.date


def user_post_directory_path(instance, filename):
    return 'profile/images/post/{0}/{1}'.format(instance.id, filename)


class UserPostModel(models.Model):
    STATUS_CHOICE = (
        (0, "PROFILE"),
        (1, "COVER"),
        (2, "ALBUMS"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICE)
    post_picture = models.ImageField(upload_to=user_post_directory_path)
    posts = models.TextField()
    title = models.CharField(max_length=200)
    amount_of_likes = models.IntegerField(default=0)
    amount_of_dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_user = models.ForeignKey(UserPostModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=1)
    dislike = models.IntegerField(default=1)

    def __str__(self):
        return self.like, self.dislike

# class DisLike(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post_user = models.ForeignKey(UserPostModel, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     dislike = models.IntegerField(default=1)
#
#     def __str__(self):
#         return self.Dislike


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_user = models.ForeignKey(UserPostModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return self.comment