from django import forms

from book.helper import is_epub
from book.models import Book


class BookEditForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('name', 'author', 'the_year_of_publishing', 'cloud_link',
                  'file', 'is_favourite', 'cover')

    def is_valid(self):
        file = self.files['file']
        if is_epub(file):
            return super().is_valid()
        else:
            return False
