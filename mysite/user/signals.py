from user_admin.models import UserCommentModel, UserImageModel, UserImageAlbumsModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone


def create_profile(instance, created, sender,  **kwargs):
    if created:
        UserCommentModel.objects.create(user=instance, date=timezone.now())


post_save.connect(receiver=create_profile, sender=User)

def create_profile_image(instance, created, sender,  **kwargs):
    if created:
        UserImageModel.objects.create(user=instance, date=timezone.now())
        UserImageAlbumsModel.objects.create(user=instance, date=timezone.now())


post_save.connect(receiver=create_profile_image, sender=User)
# post_save.connect(receiver=create_profile_image, sender=User)