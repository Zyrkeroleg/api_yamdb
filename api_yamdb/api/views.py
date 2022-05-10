from rest_framework import viewsets, mixins, filters
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Genres, Categories, Titles
from .serializers import GenreSerializer, CategorySerializer, TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('category', 'genre', 'name', 'year')


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
