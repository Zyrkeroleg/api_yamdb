from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import UserViewSet, get_jwt_token, sending_mail

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)

router_v1 = SimpleRouter()
router_v1.register(r"categories", CategoryViewSet, basename="categories")
router_v1.register(r"genres", GenreViewSet, basename="genres")
router_v1.register(r"titles", TitleViewSet, basename="titles")
router_v1.register(r"users", UserViewSet, basename="users")
router_v1.register(
    r"titles/(?P<title_id>[^/.]+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/signup/", sending_mail),  # отправка сообщения на почту
    path("v1/auth/token/", get_jwt_token),
    path(
        "v1/auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"),
]
