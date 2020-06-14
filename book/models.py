from typing import Iterable

from django.db import models
from ebooklib import epub
from ebooklib.epub import EpubException

from account.models import Profile
#  получению списка всего каталога загруженных книг,
#  списка книг, добавленных пользователем в избранное
#  и собственно API для добавления и удаления книг из избранного
from book.exceptions import NotEpubFile


class VisibleBooksManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(hidden=False)


class Book(models.Model):
    objects = models.Manager()
    visible = VisibleBooksManager()

    name = models.TextField(verbose_name='Название', max_length=400)
    cloud_link = models.URLField(verbose_name='Ссылка на облако')
    public_link = models.URLField(verbose_name='Публичная ссылка')
    loaded_by = models.ForeignKey(
        Profile,
        verbose_name='Кем загружена',
        on_delete=models.CASCADE)
    loaded_date = models.DateTimeField(verbose_name='Дата загрузки',
                                       auto_now_add=True)
    author = models.TextField(verbose_name='Автор', max_length=400, default='')
    is_favourite = models.BooleanField(verbose_name='В избранных для текущего пользователя', default=True)
    file = models.FileField(verbose_name='Файл книги', upload_to='books/%Y/%m')
    the_year_of_publishing = models.IntegerField(default=0)
    cover = models.ImageField(verbose_name='Обложка', null=True,
                              upload_to='cover/%Y/%m')
    hidden = models.BooleanField(verbose_name='Скрыта', default=False)
    language = models.CharField(verbose_name='Язык', null=True, max_length=3)
    description = models.TextField(verbose_name='Описание', null=True,
                                   max_length=1000)

    def save(self, *args, **kwargs):
        try:
            book = epub.read_epub(self.file)
        except EpubException as exc:
            raise NotEpubFile(msg=exc)

        fields = {
            'name': ['DC', 'title'],
            'language': ['DC', 'language'],
            'year_of_publishing': ['DC', 'date'],
        }

        # пока без обложки
        # cover = list(book.get_items_of_type(ebooklib.ITEM_COVER))
        # if not cover:
        #     cover = list(book.get_items_of_type(ebooklib.ITEM_IMAGE))
        #     if cover:
        #         cover = cover[0]
        # self.cover = cover

        for field, keys in fields.items():
            self.get_metadata(book, field, *keys)

        super(Book, self).save(args, kwargs)

    def get_metadata(self, book, field, namespace, key):
        value = book.get_metadata(namespace, key)
        if value:
            while isinstance(value, Iterable) and not isinstance(value, str):
                value = value[0]
            setattr(self, field, value)


class FavouriteVisibleBooksManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(book__hidden=False)


class FavouriteBooks(models.Model):
    objects = models.Manager()
    visible = FavouriteVisibleBooksManager()

    profile = models.ForeignKey(Profile, verbose_name='Пользователь',
                                on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name='Книга', on_delete=models.CASCADE)

