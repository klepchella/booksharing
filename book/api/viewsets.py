from copy import copy
from datetime import datetime
from distutils.util import strtobool

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from book.api.serializers import BookSerializer
from book.models import Book, FavouriteBooks


class BookViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def list(self, request):
        queryset = Book.visible.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def retrieve(self, request, pk=None):
        queryset = Book.visible.all()
        book = get_object_or_404(queryset, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_or_update(self, request, *args, **kwargs):
        post_params = dict(copy(request.POST))
        create = strtobool(post_params.pop('create', True)[0])
        book = Book(**post_params)

        result = {
            'success': False,
            'error_message': '',
        }

        try:
            book.file = request.FILES['file']
        except KeyError:
            result['error_message'] = (
                'Файл с книгой не обнаружен!'
            )
            return Response(result)
        book.cover = request.FILES.get('cover', None)
        book.pk = kwargs.pop('pk')
        book.loaded_by_id = request.user.profile.id

        if create:
            try:
                book.save()
                FavouriteBooks.objects.create(
                    profile_id=request.user.profile.id,
                    book_id=book.id,
                )
            except IntegrityError as ex:
                result['error_message'] = 'Книга с подобным id уже загружена!'
                return Response(result)
        else:
            book.loaded_date = datetime.now()
            book.save()
            result['success'] = True

        return Response(result)

    @action(detail=True, methods=['post'])
    def delete(self, request, pk, *args, **kwargs):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response({
            'is_deleted': True
        })

    @action(detail=True, methods=['post'])
    def download(self, request, pk, *args, **kwargs):
        try:
            book = Book.visible.get(pk=pk)
        except ObjectDoesNotExist:
            response = Response({
                'success': False,
                'error_message': 'Книга с таким id не найдена!'
            })
        else:
            response = HttpResponse(book.file, content_type='text/plain')
            response['Content-Disposition'] = (
                f'attachment; filename={book.file}'
            )

        return response

    @action(detail=False, methods=['get'])
    def list_uploaded(self, request, *args, **kwargs):
        queryset = Book.visible.filter(
            loaded_by_id=request.user.profile.id)
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)
