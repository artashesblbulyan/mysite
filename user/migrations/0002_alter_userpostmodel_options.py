# Generated by Django 4.0.2 on 2022-03-25 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userpostmodel',
            options={'ordering': ['-date']},
        ),
    ]