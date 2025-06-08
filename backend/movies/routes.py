from rest_framework.routers import DefaultRouter
from movies.views.movie_view import MovieViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movies')

urlpatterns = router.urls
