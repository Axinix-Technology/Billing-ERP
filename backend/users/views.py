import datetime
import jwt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


def serialize_user(user):
    role_name = user.role.name if user.role else ("admin" if user.is_superadmin else "cashier")
    display_name = user.name or f"{user.first_name} {user.last_name}".strip() or user.username
    return {
        "id": user.id,
        "username": user.username,
        "name": display_name,
        "role": role_name,
        "is_superadmin": user.is_superadmin,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = (request.data.get("username") or "").strip()
        password = (request.data.get("password") or "").strip()

        if not username or not password:
            return Response(
                {
                    "success": False,
                    "message": "Please enter both your username and password to sign in.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)
        if not user:
            matched_user = User.objects.select_related("role").filter(
                username__iexact=username,
                is_deleted=False,
                is_active=True,
            ).first()
            if matched_user and matched_user.check_password(password):
                user = matched_user

        if not user or user.is_deleted or not user.is_active:
            return Response(
                {
                    "success": False,
                    "message": "Invalid username or password. Please verify your login details and try again.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        Token.objects.get_or_create(user=user)
        user_data = serialize_user(user)

        jwt_payload = {
            "id": user.id,
            "username": user.username,
            "name": user_data["name"],
            "role": user_data["role"],
            "is_superadmin": user.is_superadmin,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(datetime.timezone.utc),
        }

        access_token = jwt.encode(jwt_payload, settings.SECRET_KEY, algorithm="HS256")

        return Response(
            {
                "success": True,
                "token": access_token,
                "user": user_data,
            },
            status=status.HTTP_200_OK,
        )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"success": False, "message": "Authentication required. Please sign in."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(
            {
                "success": True,
                "user": serialize_user(request.user),
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user and request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
        return Response({"success": True, "message": "Signed out successfully."})

