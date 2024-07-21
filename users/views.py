from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView

from users.models import User
from users.serliazers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)  # Убедитесь, что разрешения AllowAny установлены

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()