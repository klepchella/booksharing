from rest_framework import routers

from account.api.viewsets import AccountViewSet
from book.api.viewsets import BookViewSet

router = routers.SimpleRouter()
router.register('books', BookViewSet)
router.register('accounts', AccountViewSet)
urlpatterns = router.urls
