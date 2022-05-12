from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from uuid import uuid4

from users.models import User
from .serializers import UserSerializer, MailSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST']) # только POST запросы 
def sending_mail(request):
    serializer = MailSerializer(data=request.data)  # подключаем сериализатор
    serializer.is_valid(raise_exception=True) # проверка валидности, если что выдаётся Response с эксепшэном
    email = serializer.data['email'] # получаем email из переданных пользователем данных
    if email not in User.objects.filter(email=email): # проверка на существование в БД
        User.objects.create_user(username=f'user_{email}', email=email) # в случае отсутствия создаём нового пользователя
    token = uuid4() # создание токена
    send_mail(      # функция по отправке email'a
        'Регистрация',
        f'Ваш код доступа {token}',
        'test@gmail.com',
        ['test_token@gmail.com']
    )
    return Response('Код выслан Вам на почту!', status=status.HTTP_200_OK)  # ответ, если всё верно
