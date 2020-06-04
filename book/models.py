from django.db import models

from account.models import Profile


class Book(models.Model):
    name = models.TextField(verbose_name='Название', max_length=400)
    cloud_link = models.URLField(verbose_name='Ссылка на облако')
    public_link = models.URLField(verbose_name='Публичная ссылка')
    loaded_by = models.ForeignKey(
        Profile,
        verbose_name='Кем загружена',
        on_delete=models.CASCADE)  # todo: а каскад ли здесь нужен?
    loaded_date = models.DateTimeField(verbose_name='Дата загрузки',
                                       auto_now_add=True)
    is_favourite = models.BooleanField(verbose_name='В избранных', default=True)
