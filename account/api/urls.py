from django.urls import path

from . import viewsets

app_name = 'accounts_api'

urlpatterns = [
    path('account/login/',
         viewsets.AccountViewSet.as_view({
             'post': 'login'
         }),
         name='account_login'),
    path('account/logout/',
         viewsets.AccountViewSet.as_view({
             'post': 'logout'
         }),
         name='account_logout'),
    path('account/registration/',
         viewsets.AccountViewSet.as_view({
             'post': 'registration'
         }),
         name='account_registration'),
]