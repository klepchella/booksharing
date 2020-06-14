import os

import requests
from django.conf import settings
from django.test import SimpleTestCase
from requests.auth import HTTPBasicAuth
from rest_framework.utils import json

from account.models import Profile
from book.models import Book

LOCAL_HOST = 'http://localhost:9000/'


class BookTest(SimpleTestCase):

    @classmethod
    def setUpClass(cls):
        cls.path_file = os.path.join(
            settings.MEDIA_ROOT,
            'books',
            '2020',
            '06',
            'Pratchett.epub'
        )

        cls.path_cover = os.path.join(
            settings.MEDIA_ROOT,
            'cover',
            '2020',
            '06',
            'cover.jpg'
        )

        cls.profile = Profile.objects.all().order_by('id')[1]
        cls.password = '123456'

        cls.book = Book(
            file=cls.path_file,
            cover=cls.path_cover,
            the_year_of_publishing=2015,
            author='Terry Pratchett',
            loaded_by=cls.profile,
        )

        cls.book.save()

    def test_book_list(self):
        response = requests.get(
            f'{LOCAL_HOST}book_api/books/list/',
            auth=HTTPBasicAuth(
                self.profile.user.username,
                self.password,
            )
        )
        text = json.loads(response.text)
        self.assertEqual(response.status_code, 200)

    def test_book_favourite_list(self):
        response = requests.get(
            f'{LOCAL_HOST}book_api/books/list_favourite/',
            auth=HTTPBasicAuth(
                self.profile.user.username,
                self.password,
            )
        )
        text = json.loads(response.text)
        self.assertEqual(response.status_code, 200)

    def test_book_to_favourite(self):
        response = requests.post(
            f'{LOCAL_HOST}book_api/books/{self.book.id}/to_favourite/',
            auth=HTTPBasicAuth(
                self.profile.user.username,
                self.password,
            ),
            data={
                'to_favourite': True,
            }
        )
        text = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(text['success'], True)
        self.assertEqual(text['error_message'], '')

    def test_book_uploaded_list(self):
        response = requests.get(
            f'{LOCAL_HOST}book_api/books/list_uploaded/',
            auth=HTTPBasicAuth(
                self.profile.user.username,
                self.password,
            )
        )
        text = json.loads(response.text)
        self.assertEqual(response.status_code, 200)

    def test_book_details(self):
        response = requests.get(
            f'{LOCAL_HOST}book_api/books/{self.book.id}/',
            auth=HTTPBasicAuth(
                self.profile.user.username,
                self.password,
            ),
        )
        text = json.loads(response.text)
        self.assertEqual(response.status_code, 200)

    def test_book_create(self):
        book_file = open(self.path_file, 'rb')

        response = requests.post(
            f'{LOCAL_HOST}book_api/books/{self.book.id+1000}/create/',
            auth=HTTPBasicAuth(
                self.profile.user.username,
                self.password,
            ),
            data={
                'public_link': self.path_file,
                'cloud_link': self.path_file,
                'create': False,
            },
            files={
                'file': book_file,
            }
        )
        book_file.close()
        text = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(text['success'])

    def test_book_update(self):

        book_file = open(self.path_file, 'rb')
        response = requests.post(
            f'{LOCAL_HOST}book_api/books/{self.book.id + 1000}/update/',
            auth=HTTPBasicAuth(
                self.profile.user.username,
                self.password,
            ),
            data={
                'public_link': self.path_file,
                'cloud_link': self.path_file,
                'create': False,
            },
            files={
                'file': book_file,
            }
        )
        book_file.close()
        text = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(text['success'])

    def test_book_download(self):
        response = requests.get(
            f'{LOCAL_HOST}book_api/books/{self.book.id}/download/',
            auth=HTTPBasicAuth(
                self.profile.user.username,
                self.password,
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)

    def test_book_delete(self):
        book = Book.visible.all().first()

        response = requests.post(
            f'{LOCAL_HOST}book_api/books/{book.id}/delete/',
            auth=HTTPBasicAuth(
                self.profile.user.username,
                self.password,
            ),
        )
        text = json.loads(response.text)
        self.assertEqual(response.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        cls.book.delete()
        super().tearDownClass()
