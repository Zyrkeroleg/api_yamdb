from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User

from .permissions import AdminOnlyPermission
from .serializers import (
    RegisterSerializer,
    TokenSerializer,
    UserSerializer,
    UserSerializerOrReadOnly,
)


@api_view(["POST"])
def sending_mail(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.create(
        username=serializer.validated_data["username"],
        email=serializer.validated_data["email"],
    )
    token = default_token_generator.make_token(user)
    user.token = token
    user.save()
    send_mail(
        "Регистрация",
        (f"Email : {user.email}\n" f"Сonfirmation_code: {token}"),
        f"{settings.CONTACT_EMAIL}",
        [user.email],
        fail_silently=False,
    )
    # ответ, если верно
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_jwt_token(request):
    """Получение токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data["username"])
    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": f"{token}"}, status=status.HTTP_200_OK)
    return Response(
        {"message": "Пользователь не обнаружен"},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnlyPermission,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "username",
    ]

    def perform_create(self, serializer):
        email = self.request.data.get("email")
        if User.objects.filter(email=email):
            return Response(
                "Email уже зарегестрирован", status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        if request.method == "GET":
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = UserSerializerOrReadOnly(
                user, data=request.data,
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
