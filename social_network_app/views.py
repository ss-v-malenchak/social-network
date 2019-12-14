from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserDataChangeForm, ProfileDataChangeForm, UserPostForm, UserPostFeedFileForm, \
    GroupCreationForm, GroupPostForm, GroupPostFeedFileForm
from django.views.generic import View
from .models import Profile, UserSubscriber, GroupSubscriber, Group, UserPost, UserPostFeedFile, GroupPost, GroupPostFeedFile
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from datetime import timedelta
from django.db.models import Q
from online_users.models import OnlineUserActivity
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from PIL import Image

def index(request):
    return render(request, 'social_network_app/index.html')

@login_required(login_url='/login/')
def profile(request):
    user_id = request.user.id
    return redirect('/user/{}'.format(user_id))


def is_image(filename):
    try:
        im = Image.open(filename)
        return True
    except IOError:
        return False

@login_required(login_url='/login/')
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    current_user = request.user
    profile = Profile.objects.get(user_id=user_id)
    server = profile.get_game_server_display()
    race = profile.get_game_race_display()
    user_activity_objects = OnlineUserActivity.get_user_activities(timedelta(minutes=3))
    online_status = True if user in (user.user for user in user_activity_objects) else False
    subscribers_count = len(UserSubscriber.objects.filter(subscription=user_id))
    subscriptions_count = len(UserSubscriber.objects.filter(user=user_id))
    subscription_status = len(UserSubscriber.objects.filter(subscription=user_id, user=current_user))
    groups_count = len(GroupSubscriber.objects.filter(user=user_id))
    posts_list = UserPost.objects.filter(author=user).order_by('-date_pub')
    posts = []
    for post in posts_list:
        files = UserPostFeedFile.objects.filter(feed=post.id)
        images = []
        others = []
        for file in files:
            if is_image(file.file):
                images.append(file)
            else:
                others.append(file)
        posts.append((post, images, others))

    return render(request, 'social_network_app/profile.html',
                  context={'profile': profile,'user': user, 'current_user': current_user, 'server': server,
                           'race': race, 'online_status': online_status, 'subscribers': subscribers_count,
                           'subscriptions': subscriptions_count, 'groups': groups_count,
                           'subscription_status': subscription_status, 'posts': posts})

class UserRegister(View):

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'social_network_app/register.html', {'form': form})

    def post(self, request):
        new_user = RegistrationForm(request.POST, request.FILES)

        if new_user.is_valid():
            new_user.save()
            return redirect('/login/')
        return render(request, 'social_network_app/register.html', {'form': new_user})


@login_required(login_url='/login/')
def user_news(request):
    return render(request, 'social_network_app/news.html')

@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/user/')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'social_network_app/change_password.html', {'form': form})


def user_subscribers(request, user_id):
    subscribers = UserSubscriber.objects.filter(subscription=user_id)
    subscribers_profiles = [(Profile.objects.get(user=subscriber.user_id), User.objects.get(id=subscriber.user_id))
                            for subscriber in subscribers]
    return render(request, 'social_network_app/subscribers-subscriptions.html',
                  context={'title': 'Subscribers', 'users': subscribers_profiles})


def user_subscription(request, user_id):
    subscriptions = UserSubscriber.objects.filter(user=user_id)
    subscriptions_profiles = [(Profile.objects.get(user=subscriber.subscription_id), User.objects.get(id=subscriber.subscription_id))
                            for subscriber in subscriptions]
    return render(request, 'social_network_app/subscribers-subscriptions.html',
                  context={'title': 'Subscriptions', 'users': subscriptions_profiles})


def user_groups(request, user_id):
    groups_list = GroupSubscriber.objects.filter(user=user_id)
    groups = [(Group.objects.get(id=group.group_id), len(GroupSubscriber.objects.filter(group=group.group))) for group in groups_list]
    create_group = True if request.user.id == user_id else False
    return render(request, 'social_network_app/groups-list.html', context={'groups': groups, 'create_group': create_group})

def groups_list(request):
    user_id = request.user.id
    return redirect('/user/{}/groups'.format(user_id))


def change_user_data(request):
    if request.method == 'POST':
        form = UserDataChangeForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/user/{}/'.format(request.user.id))
    else:
        form = UserDataChangeForm(instance=request.user)
    return render(request, 'social_network_app/change-user-data.html', {'title': 'user', 'form': form})

def change_profile_data(request):
    if request.method == 'POST':
        form = ProfileDataChangeForm(data=request.POST, instance=Profile.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            return redirect('/user/{}/'.format(request.user.id))
    else:
        form = ProfileDataChangeForm(instance=Profile.objects.get(user=request.user))

    return render(request, 'social_network_app/change-user-data.html', {'title': 'profile', 'form': form})


def create_new_user_post(request):
    user = request.user
    if request.method == 'POST':
        form = UserPostForm(request.POST)
        file_form = UserPostFeedFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')  # field name in model
        if form.is_valid() and file_form.is_valid():
            feed_instance = form.save(commit=False)
            feed_instance.author = user
            feed_instance.save()
            for f in files:
                file_instance = UserPostFeedFile(file=f, feed=feed_instance)
                file_instance.save()
        return redirect('/user/{}/'.format(request.user.id))
    else:
        form = UserPostForm()
        file_form = UserPostFeedFileForm()

    return render(request, 'social_network_app/create-post.html', {'file_form': file_form, 'form': form})


def create_new_group(request):
    if request.method == 'POST':
        form = GroupCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_group = form.save(request.user)
            new_group.admin = request.user
            new_group.save()
            return redirect('/group/{}/'.format(new_group.id))
    else:
        form = GroupCreationForm()

    return render(request, 'social_network_app/create-group.html', {'form': form})

def create_new_group_post(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.method == 'POST':
        form = GroupPostForm(request.POST)
        file_form = GroupPostFeedFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        if form.is_valid() and file_form.is_valid():
            feed_instance = form.save(commit=False)
            feed_instance.author = group
            feed_instance.save()
            for f in files:
                file_instance = GroupPostFeedFile(file=f, feed=feed_instance)
                file_instance.save()
        return redirect('/group/{}/'.format(request.user.id))
    else:
        form = GroupPostForm()
        file_form = GroupPostFeedFileForm()

    return render(request, 'social_network_app/create-post.html', {'file_form': file_form, 'form': form})

def group(request, group_id):
    current_user = request.user
    group = Group.objects.get(id=group_id)
    admin = User.objects.get(id=group.admin_id)
    subscribers_list = GroupSubscriber.objects.filter(group=group)
    subscribers = [(subscriber, User.objects.get(id=subscriber.user_id),
                    Profile.objects.filter(user=subscriber.user_id)) for subscriber in subscribers_list]
    subscription_status = False
    for subscriber in subscribers_list:
        if subscriber.user == current_user:
            subscription_status = True
            break
    posts_list = GroupPost.objects.filter(author=group_id).order_by('-date_pub')
    posts = []
    for post in posts_list:
        files = GroupPostFeedFile.objects.filter(feed=post.id)
        images = []
        others = []
        for file in files:
            if is_image(file.file):
                images.append(file)
            else:
                others.append(file)
        posts.append((post, images, others))

    return render(request, 'social_network_app/group.html',
                  context={'user': current_user, 'group': group, 'admin': admin, 'subscribers': len(subscribers),
                            'subscription_status': subscription_status, 'posts': posts})


def group_subscribers(request, group_id):
    group = Group.objects.get(id=group_id)
    subscribers_list = GroupSubscriber.objects.filter(group=group)
    subscribers_profiles = [(Profile.objects.get(user=subscriber.user_id), User.objects.get(id=subscriber.user_id))
                            for subscriber in subscribers_list]
    return render(request, 'social_network_app/subscribers-subscriptions.html',
                  context={'title': '{} subscribers'.format(group.name), 'users': subscribers_profiles})

def find_user(request):
    query = request.GET.get('q')
    qs = User.objects.all()
    for term in query.split():
        qs = qs.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term))
    users_data = [(Profile.objects.get(user=user.id), User.objects.get(id=user.id))
                            for user in qs]
    return render(request, 'social_network_app/subscribers-subscriptions.html',
                  context={'title': 'Finded users', 'users': users_data})



