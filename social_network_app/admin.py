from django.contrib import admin
from .models import Profile, Group

class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile)


class GroupAdmin(admin.ModelAdmin):
    pass

admin.site.register(Group)