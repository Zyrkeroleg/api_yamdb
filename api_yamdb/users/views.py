from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.core.mail import send_mail
from uuid import uuid4
from users.models import User
from .serializers import UserSerializer, UserSerializerOrReadOnly, RegisterSerializer, TokenSerializer
from .validators import email_validator
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import AdminOnlyPermission
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken

@api_view(['POST']) # только POST запросы 
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
    return Response(serializer.data, status=status.HTTP_200_OK)  # ответ, если всё верно


@api_view(['POST'])
def get_jwt_token(request):
    """Получение токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User,username=serializer.validated_data['username'])
    if default_token_generator.check_token(
        user,
        serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response(
            {'token': f'{token}'},
            status=status.HTTP_200_OK
        )
    return Response(
        {'message': 'Пользователь не обнаружен'},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnlyPermission,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]

    def create(self, request, *args, **kwargs):
        if not request.data.get('email'):
            return Response('Поле email обязательно', status=status.HTTP_400_BAD_REQUEST)
        email = request.data.get('email')
        print(email)
        if User.objects.filter(email=email):
            return Response('Email уже зарегестрирован', status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)

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