from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from account.helpers import get_current_user_id
from book.forms import BookEditForm
from book.helper import get_favourite_books, get_uploaded_books
from book.models import Book


@login_required
def load_book(request):
    if request.method == 'POST':
        load_book_form = BookEditForm(request.POST, request.FILES)
        if load_book_form.is_valid():
            cleaned_data = load_book_form.cleaned_data

            book = Book(**cleaned_data)
            # book.cover_id = cover.id
            book.loaded_by_id = get_current_user_id(request)
            book.save()
            return render(
                request,
                'book/load_book_done.html',
                {
                    'book': book,
                }
            )
        else:
            messages.error(request, 'File is not Epub!')
    else:
        load_book_form = BookEditForm()
    return render(
        request,
        'book/load_book.html',
        {
            'form': load_book_form,
        }
    )


@login_required
def favourite_books(request):
    return render(
        request,
        'book/list_books.html',
        {
            'books': get_favourite_books(),
            'books_type': 'favourite',
        },
    )


@login_required
def uploaded_books(request):
    return render(
        request,
        'book/list_books.html',
        {
            'books': get_uploaded_books(request),
            'books_type': 'uploaded',
         },
    )
