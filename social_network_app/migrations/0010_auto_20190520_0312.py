# Generated by Django 2.2.1 on 2019-05-20 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network_app', '0009_auto_20190520_0241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, db_index=True, max_length=50),
        ),
    ]
