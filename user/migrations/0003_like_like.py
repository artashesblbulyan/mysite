# Generated by Django 4.0.2 on 2022-03-20 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='like',
            field=models.IntegerField(default=1),
        ),
    ]
