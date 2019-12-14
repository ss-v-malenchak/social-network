from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .choices import *
from .models import Profile, UserPost, UserPostFeedFile, Group, GroupPost, GroupPostFeedFile
from django.forms import ClearableFileInput


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    nickname = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nickname'}))
    game_server = forms.ChoiceField(choices=SERVER_CHOICES, required=True, widget=forms.Select(
        attrs={'class': 'form-control', 'placeholder': 'Game server'}))
    game_race = forms.ChoiceField(choices=RACE_CHOICES, required=True, widget=forms.Select(
        attrs={'class': 'form-control', 'placeholder': 'Game race'}))
    game_alliance = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Game alliance'}))
    game_guild = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Game guild'}))
    game_class = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Game class'}))
    character_equip_calculator = forms.URLField(widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'Character equip calculator'}))
    about_user = forms.CharField(max_length=1024, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'About me'}))
    avatar = forms.ImageField()
    wallpaper = forms.ImageField()


    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'nickname', 'game_server',
                  'game_race', 'game_alliance', 'game_guild', 'game_class', 'character_equip_calculator', 'about_user',
                  'avatar', 'wallpaper')

    def save(self):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        user_profile = Profile.objects.create(
            user=user,
            nickname=self.cleaned_data['nickname'],
            game_server=self.cleaned_data['game_server'],
            game_race=self.cleaned_data['game_race'],
            game_alliance=self.cleaned_data['game_alliance'],
            game_guild=self.cleaned_data['game_guild'],
            game_class=self.cleaned_data['game_class'],
            character_equip_calculator=self.cleaned_data['character_equip_calculator'],
            about_user=self.cleaned_data['about_user'],
            avatar=self.cleaned_data['avatar'],
            wallpaper=self.cleaned_data['wallpaper']
        )
        return user_profile


class UserDataChangeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileDataChangeForm(forms.ModelForm):
    nickname = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nickname'}))
    game_server = forms.ChoiceField(choices=SERVER_CHOICES, required=True, widget=forms.Select(
        attrs={'class': 'form-control', 'placeholder': 'Game server'}))
    game_race = forms.ChoiceField(choices=RACE_CHOICES, required=True, widget=forms.Select(
        attrs={'class': 'form-control', 'placeholder': 'Game race'}))
    game_alliance = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Game alliance'}))
    game_guild = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Game guild'}))
    game_class = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Game class'}))
    character_equip_calculator = forms.URLField(widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'Character equip calculator'}))
    about_user = forms.CharField(max_length=1024, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'About me'}))
    avatar = forms.ImageField()
    wallpaper = forms.ImageField()

    class Meta:
        model = Profile
        fields = ('nickname', 'game_server', 'game_race', 'game_alliance', 'game_guild', 'game_class',
                  'character_equip_calculator', 'about_user', 'avatar', 'wallpaper')


class UserPostForm(forms.ModelForm):
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'Title'}))
    text_content = forms.CharField(max_length=1024, widget=forms.Textarea(attrs={'class': 'form-control',
                                                                                'placeholder': 'About me'}))

    class Meta:
        model = UserPost
        fields = ['title', 'text_content']


class UserPostFeedFileForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = UserPostFeedFile
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }


class GroupCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Group name'}))
    activities = forms.CharField(max_length=1024, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'About group'}))
    avatar = forms.ImageField()
    wallpaper = forms.ImageField()

    class Meta:
        model = Group
        fields = ('name', 'activities', 'avatar', 'wallpaper')


    def save(self, admin):
        group = Group.objects.create(
            name=self.cleaned_data['name'],
            admin=admin,
            activities=self.cleaned_data['activities'],
            avatar=self.cleaned_data['avatar'],
            wallpaper=self.cleaned_data['wallpaper']
        )
        return group

class GroupPostForm(forms.ModelForm):
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'Title'}))
    text_content = forms.CharField(max_length=1024, widget=forms.Textarea(attrs={'class': 'form-control',
                                                                                'placeholder': 'About me'}))

    class Meta:
        model = GroupPost
        fields = ['title', 'text_content']


class GroupPostFeedFileForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = GroupPostFeedFile
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }
