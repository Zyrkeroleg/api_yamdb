from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Categories, Genres, Review, Title

from .filters import TitleFilter
from .pagination import CustomCommentPagination, CustomReviewPagination
from .permissions import (
    AdminOnlyPermission,
    ReviewsComentsPermission,
    SafeMethodsOnlyPermission,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    http_method_names = ["get", "post", "head", "patch", "delete"]
    filter_class = TitleFilter
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOnlyPermission,)

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH"):
            return TitlePostSerializer
        return TitleGetSerializer


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    pagination_class = LimitOffsetPagination
    permission_classes = (SafeMethodsOnlyPermission,)
    lookup_field = "slug"


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    pagination_class = LimitOffsetPagination
    permission_classes = (SafeMethodsOnlyPermission,)
    lookup_field = "slug"


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (ReviewsComentsPermission,)
    pagination_class = CustomReviewPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (ReviewsComentsPermission,)
    pagination_class = CustomCommentPagination

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)
