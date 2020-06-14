from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from account.messages import LOGIN_SUCCESSFUL, LOGIN_FAILED, LOGOUT_SUCCESSFUL, \
    LOGOUT_ALREADY, USER_ALREADY_EXISITS, REGISTRATION_SUCCESSFUL
from account.models import Profile


class AccountViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        result = {'success': False, 'message': ''}
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session.set_expiry(settings.SESSION_LIVE_TIME)
            request.session['name'] = username
            # request.session.create()
            result['success'] = True
            result['message'] = LOGIN_SUCCESSFUL
        else:
            result['message'] = LOGIN_FAILED
        return Response(result)

    @action(detail=False, methods=['post'])
    def logout(self, request, *args, **kwargs):
        user = request.user
        result = {'success': False, 'message': ''}
        if user.is_authenticated or request.session.session_key:
            request.session.delete(request.session.session_key)
            logout(request)
            result['success'] = True
            result['message'] = LOGOUT_SUCCESSFUL
        else:
            result['success'] = False
            result['message'] = LOGOUT_ALREADY
        return Response(result)

    @action(detail=False, methods=['post'])
    def registration(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        result = {'success': False, 'message': ''}

        is_user_exists = User.objects.filter(username=username).exists()
        if is_user_exists:
            result['message'] = USER_ALREADY_EXISITS
        else:
            user = User.objects.create_user(username, password=password)
            profile = Profile.objects.create(user=user)
            user.is_superuser = False
            user.is_staff = False
            user.save()
            result['success'] = True
            result['message'] = REGISTRATION_SUCCESSFUL
        return Response(result)



