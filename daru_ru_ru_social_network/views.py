from django.shortcuts import render
from django.contrib.auth.models import User
from django_private_chat.models import Dialog
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def get_users_dialog(dialog):
    dialog  = User.objects.get(id=dialog.opponent_id)


@login_required(login_url='/login/')
def user_dialogs(request):
    dialogs_list = Dialog.objects.filter(Q(owner_id=request.user.id) | Q(opponent_id=request.user.id))
    print(dialogs_list)
    profiles = apps.get_model('social_network_app', 'Profile')
    opponents_profiles = [(profiles.objects.get(user_id=dialog.opponent_id if dialog.opponent_id != request.user.id else dialog.owner_id),
                           User.objects.get(id=dialog.opponent_id if dialog.opponent_id != request.user.id else dialog.owner_id))
                          for dialog in dialogs_list]
    print(opponents_profiles)
    return render(request, 'social_network_app/dialogs_list.html', context={'opponents': opponents_profiles})