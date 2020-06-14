from django.urls import path

from . import views, viewsets

app_name = 'books_api'


urlpatterns = [
    path('books/list/',
         viewsets.BookViewSet.as_view({'get': 'list', }),
         name='books_list'),

    path('books/list_favourite/',
         views.BookFavouriteListView.as_view(),
         name='books_favourite_list'),

    path('books/<pk>/to_favourite/',
         views.BookAddInFavouriteView.as_view(),
         name='book_to_favourite'),

    path('books/list_uploaded/',
         viewsets.BookViewSet.as_view({'get': 'list_uploaded',}),
         name='books_favourite_list'),

    path('books/<pk>/',
         viewsets.BookViewSet.as_view({'get': 'retrieve',}),
         name='book_detail'),

    path('books/<pk>/create/',
         viewsets.BookViewSet.as_view({'post': 'create_or_update',}),
         name='create'),

    path('books/<pk>/update/',
         viewsets.BookViewSet.as_view({'post': 'create_or_update',}),
         name='update'),

    path('books/<pk>/delete/',
         viewsets.BookViewSet.as_view({'post': 'delete'}),
         name='delete_books'),

    path('books/<pk>/download/',
         viewsets.BookViewSet.as_view({'get': 'download'}),
         name='download_books'),
]
