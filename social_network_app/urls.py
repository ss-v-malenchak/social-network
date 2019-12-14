from django.urls import path
from .views import index, UserRegister, profile, user_profile, user_news, change_password,\
    user_subscribers, user_subscription, user_groups, groups_list, change_user_data, change_profile_data,\
    create_new_user_post, create_new_group, create_new_group_post, group, group_subscribers, find_user

from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', index, name='index_url'),
    path('register/', UserRegister.as_view(), name='register_url'),
    path('login/', LoginView.as_view(template_name='social_network_app/login.html'), name='login_url'),
    path('logout/', LogoutView.as_view(template_name='social_network_app/logout.html'), name='logout_url'),
    path('user/', profile, name='current_user_profile_url'),
    path('user/<user_id>/', user_profile, name="user_page_url"),
    path('news/', user_news, name="user_news_url"),
    path('change-password/', change_password, name="change_password_url"),
    path('user/<user_id>/subscribers/', user_subscribers, name="user_subscribers_url"),
    path('user/<user_id>/subscription/', user_subscription, name="user_subscription_url"),
    path('user/<user_id>/groups/', user_groups, name="user_groups_url"),
    path('groups/', groups_list, name="group_list_url"),
    path('change-user-data/', change_user_data, name="change_user_data_url"),
    path('change-profile-data/', change_profile_data, name="change_profile_data_url"),
    path('create-new-user-post/', create_new_user_post, name="create_new_user_post_url"),
    path('create-group/', create_new_group, name="create_new_group_url"),
    path('group/<group_id>/create-new-group-post/', create_new_group_post, name="create_new_group_post_url"),
    path('group/<group_id>/', group, name='group_url'),
    path('group/<group_id>/subscribers/', group_subscribers, name='group_subscribers_url'),
    path('find-user/', find_user, name='find_user_url')
]
