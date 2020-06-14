import random

import requests
from django.contrib.auth.models import User
from django.test import SimpleTestCase
from requests.auth import HTTPBasicAuth
from rest_framework.utils import json

from account import messages
from account.models import Profile

LOCAL_HOST = 'http://localhost:9000/'


class ProfileTest(SimpleTestCase):
    username = 'test_user'
    password = 'password'

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username=cls.username,
            password=cls.password)
        cls.profile = Profile.objects.create(user_id=cls.user.id)

    def test_registration_already_exists(self):
        response = requests.post(
            f'{LOCAL_HOST}account_api/account/registration/',
            data={
                'username': self.username,
                'password': self.password,
            },
        )
        text = json.loads(response.text)
        self.assertEqual(text['success'], False)
        self.assertEqual(text['message'], messages.USER_ALREADY_EXISITS)

    def test_registration(self):
        response = requests.post(
            f'{LOCAL_HOST}account_api/account/registration/',
            data={
                'username': f'new_user_{random.randint(1, 999999)}',
                'password': 'password',
            },
        )
        text = json.loads(response.text)
        self.assertEqual(text['success'], True)
        self.assertEqual(text['message'], messages.REGISTRATION_SUCCESSFUL)

    def test_login(self):
        response = requests.post(
            f'{LOCAL_HOST}account_api/account/login/',
            data={
                'username': self.user,
                'password': self.password,
            },
        )
        text = json.loads(response.text)
        self.assertEqual(text['success'], True)
        self.assertEqual(text['message'], messages.LOGIN_SUCCESSFUL)

    def test_logout(self):
        response = requests.post(
            f'{LOCAL_HOST}account_api/account/logout/',
            auth=HTTPBasicAuth(
                self.user.username,
                self.password,
            )
        )
        text = json.loads(response.text)
        self.assertEqual(text['success'], True)
        self.assertEqual(text['message'], messages.LOGOUT_SUCCESSFUL)

    @classmethod
    def tearDownClass(cls):
        cls.profile.delete()
        cls.user.delete()
