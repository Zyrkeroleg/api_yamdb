import django_filters
from reviews.models import Categories, Genres, Title


class TitleFilter(django_filters.FilterSet):
    """Переопределение названия полей с помощью создания custom filter"""

    genre = django_filters.ModelMultipleChoiceFilter(
        queryset=Genres.objects.all(),
        field_name="genre__slug", to_field_name="slug"
    )
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Categories.objects.all(),
        field_name="category__slug",
        to_field_name="slug",
    )
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains")

    class Meta:
        model = Title
        fields = ["genre", "category", "name", "year"]
