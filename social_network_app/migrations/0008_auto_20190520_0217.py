# Generated by Django 2.2.1 on 2019-05-19 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_network_app', '0007_profile_wallpaper'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentfiles',
            name='feed',
        ),
        migrations.RemoveField(
            model_name='group',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='group',
            name='subscribers',
        ),
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.RemoveField(
            model_name='postfiles',
            name='feed',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='CommentFiles',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='PostFiles',
        ),
    ]