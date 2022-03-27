from user.models import UserImageModel, UserImageAlbumsModel, Comment
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone


# def create_profile(instance, created, sender,  **kwargs):
#     if created:
#         Comment.objects.create(user=instance, created_at=timezone.now())
#
#
# post_save.connect(receiver=create_profile, sender=User)


def create_profile_image(instance, created, sender,  **kwargs):
    if created:
        UserImageModel.objects.create(user=instance, created_at=timezone.now())


post_save.connect(receiver=create_profile_image, sender=User)


def create_album_image(instance, created, sender,  **kwargs):
    if created:
        UserImageAlbumsModel.objects.create(user=instance, created_at=timezone.now(), status=0)


post_save.connect(receiver=create_album_image, sender=User)

