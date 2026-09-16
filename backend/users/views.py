from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    LoginSerializer,
    PasswordChangeSerializer,
    UserRegisterSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from .services.auth_service import AuthService
from .services.token_service import TokenService
from .services.user_service import UserService


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = AuthService.register(**serializer.validated_data)
        tokens = TokenService.issue_tokens_for_user(user)

        return Response({"tokens": tokens, "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = AuthService.login(
            credential=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        tokens = TokenService.issue_tokens_for_user(user)

        return Response({"tokens": tokens, "user": UserSerializer(user).data}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"detail": "refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

        TokenService.blacklist(refresh)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        UserService.change_user_password(user=request.user, new_password=serializer.validated_data["new_password"])

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UserUpdateSerializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = UserService.update_profile(user=request.user, **serializer.validated_data)

        return Response(UserSerializer(user).data)


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

        tokens = TokenService.refresh(refresh_token)
        return Response(tokens, status=status.HTTP_200_OK)
