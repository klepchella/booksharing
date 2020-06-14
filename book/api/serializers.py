from rest_framework import serializers

from account.models import Profile
from book.models import Book, FavouriteBooks


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id', 'user_id', 'date_of_birth',
            'photo',
        ]


class BookSerializer(serializers.ModelSerializer):
    loaded_by = ProfileSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'the_year_of_publishing',
                  'file', 'is_favourite', 'cloud_link',
                  'public_link', 'loaded_by', 'loaded_date', 'cover']


class FavouriteBooksSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer
    book = BookSerializer

    class Meta:
        model = FavouriteBooks
        fields = ('book',)