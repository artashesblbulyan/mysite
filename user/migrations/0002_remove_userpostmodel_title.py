# Generated by Django 4.0.2 on 2022-04-11 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpostmodel',
            name='title',
        ),
    ]