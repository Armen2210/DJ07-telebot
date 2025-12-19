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
    serializer = TelegramUserSerializer(user)
    return Response(serializer.data)

