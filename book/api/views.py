from distutils.util import strtobool

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from book.api.serializers import FavouriteBooksSerializer
from book.models import Book, FavouriteBooks


class BookFavouriteListView(generics.ListAPIView):
    queryset = FavouriteBooks.visible.all()
    serializer_class = FavouriteBooksSerializer

    def get(self, request, *args, **kwargs):
        queryset = FavouriteBooks.visible.filter(
            profile_id=request.user.profile.id,
        ).select_related('book')
        serializer = FavouriteBooksSerializer(queryset, many=True)
        return Response(serializer.data)


class BookApi(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class BookAddInFavouriteView(BookApi):

    def post(self, request, pk, *args, **kwargs):
        book = get_object_or_404(Book, pk=pk)
        to_favourite = strtobool(request.POST.get('to_favourite', True))
        profile_id = request.user.profile.id

        result = {
            'error_message': '',
            'success': False,
        }
        if to_favourite:
            fav_book, created = FavouriteBooks.objects.get_or_create(
                book_id=book.id,
                profile_id=profile_id
            )
            fav_book.save()
            result['success'] = True
        else:
            try:
                fav_book = FavouriteBooks.visible.get(
                    book_id=book.id,
                    profile_id=profile_id
                )
            except ObjectDoesNotExist:
                result['error_message'] = (
                    'Эта книга не найдена у вас в избранных!')
                return result
            else:
                fav_book.delete()
                result['success'] = True

        if book.loaded_by_id == profile_id:
            book.is_favourite = to_favourite
            book.save()

        return Response(result)

    def get(self, request, pk, *args, **kwargs):
        book = get_object_or_404(Book, pk=pk)
        return Response({
            'book_id': book.id,
            'is_favourite': book.is_favourite,
        })
