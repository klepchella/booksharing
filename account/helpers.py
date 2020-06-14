from account.models import Profile


def get_current_user_id(request):
    return Profile.objects.get(user_id=request.user.id).id
