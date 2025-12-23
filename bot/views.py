from rest_framework.decorators import api_view
from rest_framework.response import Response
# между скачанными модулями и личными ставится отступ: сначала скачанные(самые первые идут питоновские)
from .models import TelegramUser
from .serializers import TelegramUserSerializer


# Create your views here.
@api_view(['POST'])
def register_user(request):
    data = request.data
    user, created = TelegramUser.objects.get_or_create(
        user_id=data['user_id'],
        defaults={
            'username': data.get('username', ''),}
    )
    if created:
        serializer = TelegramUserSerializer(user)
        return Response(serializer.data)
    else:
        return Response({'error': 'User already exists'}, status=400)


@api_view(['GET'])
def get_user_info(request, user_id):
    try:
        user = TelegramUser.objects.get(user_id=user_id)
        serializer = TelegramUserSerializer(user)
        return Response(serializer.data)
    except TelegramUser.DoesNotExist:
        return Response({'message': 'User not found'}, status=404)
