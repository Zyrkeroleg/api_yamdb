from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.core.mail import send_mail
from uuid import uuid4
from users.models import User
from .serializers import UserSerializer, MailSerializer, UserSerializerOrReadOnly
from .validators import email_validator
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import AdminOnlyPermission
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
    

@api_view(['POST']) # только POST запросы 
def sending_mail(request):
    serializer = MailSerializer(data=request.data)  # подключаем сериализатор
    serializer.is_valid(raise_exception=True) # проверка валидности, если что выдаётся Response с эксепшэном
    username = request.data.get('username')
    email = request.data.get('email')
    if email in User.objects.filter(email=email): # проверка на существование в БД
        raise ValidationError('Пользователь уже создан')
    token = uuid4() # создание токена
    User.objects.get_or_create(username=username, email=email, token=token) # в случае отсутствия создаём нового пользователя
    send_mail(
        'Регистрация',
        (f'Email : {email}\n'
         f'Сonfirmation_code: {token}'),
        f'{settings.CONTACT_EMAIL}',
        [email],
        fail_silently=False,
    )
    return Response('Код выслан Вам на почту!', status=status.HTTP_200_OK)  # ответ, если всё верно


@api_view(['POST'])
def get_jwt_token(request):
    """Получение токена."""
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    user = get_object_or_404(User,username=username)
    if not confirmation_code or not username:
        raise ValidationError(
            {
                'info': 'confirmation_code и username\n'
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