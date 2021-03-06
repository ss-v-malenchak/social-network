# Generated by Django 2.2.1 on 2019-05-19 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network_app', '0008_auto_20190520_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='about_user',
            field=models.TextField(blank=True, default='', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='character_equip_calculator',
            field=models.URLField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='game_alliance',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='game_class',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='game_guild',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='game_race',
            field=models.CharField(choices=[('NN', 'None'), ('NU', 'Nuian'), ('EL', 'Elf'), ('DW', 'Dwarf'), ('FR', 'Firran'), ('HR', 'Narani'), ('WB', 'Warborn')], default='NN', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='game_server',
            field=models.CharField(choices=[('NON', 'None'), ('LCS', 'Lucius'), ('ARI', 'Aria'), ('SHD', 'Shaeda'), ('KLE', 'Kaile'), ('NUI', 'Nui'), ('HZE', 'Haze'), ('KRV', 'Korvus'), ('FNM', 'Fanem')], default='NON', max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='wallpaper',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
    ]
