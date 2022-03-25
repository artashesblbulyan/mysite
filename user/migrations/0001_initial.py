# Generated by Django 4.0.2 on 2022-03-25 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPostModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('post_picture', models.ImageField(upload_to=user.models.user_post_directory_path)),
                ('posts', models.TextField()),
                ('title', models.CharField(max_length=200)),
                ('amount_of_likes', models.IntegerField(default=0)),
                ('amount_of_dislikes', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='UserImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('profile_picture', models.ImageField(blank=True, default='/a1.jpg', null=True, upload_to=user.models.user_image_directory_path)),
                ('cover_photo', models.ImageField(blank=True, default='/cover_photo.jpg', null=True, upload_to=user.models.user_image_directory_path)),
                ('photo_albums', models.ImageField(blank=True, null=True, upload_to=user.models.user_image_directory_path)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserImageAlbumsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'PROFILE'), (1, 'COVER'), (2, 'ALBUMS')])),
                ('profile_picture', models.ImageField(default='/a1.jpg', upload_to=user.models.user_image_directory_path)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('like', models.IntegerField(default=1)),
                ('dislike', models.IntegerField(default=1)),
                ('post_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userpostmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('post_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userpostmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('category', models.IntegerField(blank=True, choices=[(0, 'Communication'), (1, 'Conference Report'), (2, 'Editorial'), (3, 'Opinion'), (4, 'Perspective'), (5, 'Book Review'), (6, 'Registered Report'), (7, 'Review'), (8, 'Else')], null=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userpostmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
