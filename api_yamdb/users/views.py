from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from uuid import uuid4
from users.models import User
from .serializers import UserSerializer, MailSerializer
from .validators import email_validator
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

@api_view(['POST']) # только POST запросы 
def sending_mail(request):
    serializer = MailSerializer(data=request.data)  # подключаем сериализатор
    serializer.is_valid(raise_exception=True) # проверка валидности, если что выдаётся Response с эксепшэном
    email = serializer.data['email'] # получаем email из переданных пользователем данных
    if email not in User.objects.filter(email=email): # проверка на существование в БД
        User.objects.get_or_create(username=f'user_{email}', email=email) # в случае отсутствия создаём нового пользователя
    token = uuid4() # создание токена
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
    email = request.data.get('email')
    email_validator(email)
    confirmation_code = request.data.get('confirmation_code')
    if not confirmation_code or not email:
        raise ValidationError(
            {
                'info': 'Заполни необходимые поля'
            }
        )
    user = get_object_or_404(User, email=email)
    result = {'info': 'Не верный код'}
    if uuid4().check_token(
            user=user,
            token=confirmation_code
    ):
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

