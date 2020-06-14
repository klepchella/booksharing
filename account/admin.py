from django.contrib import admin

# Register your models here.
from account.models import Profile
from book.models import Book, FavouriteBooks


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'the_year_of_publishing', 'cloud_link',
                    'file', 'cover']


@admin.register(FavouriteBooks)
class FavouriteBooksAdmin(admin.ModelAdmin):
    list_display = ['profile', 'book']