# from uuid import uuid4

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
# from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User

from .permissions import AdminOnlyPermission
from .serializers import (RegisterSerializer, UserSerializer,
                          UserSerializerOrReadOnly)

# from .validators import email_validator


@api_view(['POST'])  # только POST запросы
def sending_mail(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.create(
        username=serializer.validated_data['username'],
        email=serializer.validated_data['email'],
    )
    token = default_token_generator.make_token(user)
    user.token = token
    user.save()
    send_mail(
        'Регистрация',
        (f'Email : {user.email}\n'
         f'Сonfirmation_code: {token}'),
        f'{settings.CONTACT_EMAIL}',
        [user.email],
        fail_silently=False,
    )
    # ответ, если всё верно
    return Response('Код выслан Вам на почту!', status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    """Получение токена."""
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if not confirmation_code or not username:
        raise ValidationError(
            {
                'info': 'confirmation_code и username '
                        'являются обязательными полями!'
            }
        )
    token = user.token
    result = {'Введите правильный confirmation_code'}
    if confirmation_code == token:
        user.is_active = True
        user.save()

        def get_tokens_for_user(current_user):
            refresh = RefreshToken.for_user(current_user)

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        result = get_tokens_for_user(user)
    return Response(result)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnlyPermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        if request.method == 'PATCH':
            serializer = UserSerializerOrReadOnly(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
