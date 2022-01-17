from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    RegisterViewSet, ReviewViewSet, TitleViewSet, TokenViewSet,
                    UsersViewSet)

router_v1 = DefaultRouter()
router_v1.register('genres', GenreViewSet, basename='genres_view')
router_v1.register('categories', CategoryViewSet, basename='categories_view')
router_v1.register('titles', TitleViewSet, basename='titles_view')
router_v1.register('auth/signup', RegisterViewSet, basename='register_view')
router_v1.register('auth/token', TokenViewSet, basename='token_view')
router_v1.register(r'users', UsersViewSet, basename='profile_view')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)


urlpatterns = [
    path('v1/', include(router_v1.urls), ),
]
