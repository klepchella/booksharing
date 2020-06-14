from ebooklib import epub
from ebooklib.epub import EpubException

from account.helpers import get_current_user_id
from book.models import Book


def is_epub(file):
    try:
        book = epub.read_epub(file)
    except EpubException:
        return False
    else:
        return True


def get_favourite_books():
    return Book.favourite_objects.all().values(
        'name',
        'author',
        'the_year_of_publishing',
        'cloud_link',
        'file',
        'cover',
        'is_favourite',
    )


def get_uploaded_books(request):
    return Book.objects.filter(loaded_by_id=get_current_user_id(request))
