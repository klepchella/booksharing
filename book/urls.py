from django.urls import path

from . import views

urlpatterns = [
    path('load_book/', views.load_book, name='load_book'),
    path('favourite_books/', views.favourite_books, name='favourite_books'),
    path('uploaded_books/', views.uploaded_books, name='uploaded_books'),
]