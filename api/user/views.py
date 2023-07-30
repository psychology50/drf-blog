from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import *

User = get_user_model()
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes_by_action = {
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'create': [AllowAny],
        'update': [IsAuthenticated],
        'destroy': [IsAuthenticated],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        reg_serializer = self.get_serializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save()

            return Response(
                {
                    "user": self.get_serializer(new_user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginUserBodySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nickname = serializer.validated_data.get("nickname")
        password = serializer.validated_data.get("password")

        if not nickname or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            nickname=nickname,
            password=password,
        )

        if user:
            token = TokenObtainPairSerializer.get_token(user)

            return Response(
                {
                    "refresh": str(token),
                    "access": str(token.access_token),
                }, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=["post"])
    def logout(self, request, *args):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        reset = ""
        res = Response({"message": "logout success"}, status=status.HTTP_204_NO_CONTENT)
        res.set_cookie("access", reset)
        res.set_cookie("refresh", reset)

        return Response({"message": "logout success"}, status=status.HTTP_204_NO_CONTENT)