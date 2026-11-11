import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.authtoken.models import Token

User = get_user_model()


class DualTokenAndBearerAuthentication(BaseAuthentication):
    """
    Seamless Dual Authentication supporting:
    1. 'Authorization: Bearer <jwt_or_key>' (standard for React frontend)
    2. 'Authorization: Token <key>' (standard for DRF / cURL clients)
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth:
            return None

        prefix = auth[0].lower().decode("utf-8")
        if prefix not in ("bearer", "token"):
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed("Invalid authorization header. No token provided.")
        if len(auth) > 2:
            raise exceptions.AuthenticationFailed("Invalid authorization header. Token must not contain spaces.")

        token_str = auth[1].decode("utf-8")

        # 1. Attempt decoding as signed JWT
        try:
            jwt_secret = settings.SECRET_KEY
            payload = jwt.decode(token_str, jwt_secret, algorithms=["HS256"])
            user_id = payload.get("id") or payload.get("user_id")
            if user_id:
                user = User.objects.select_related("role").filter(pk=user_id, is_deleted=False).first()
                if user and user.is_active:
                    return (user, token_str)
        except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
            pass

        # 2. Attempt matching as DRF Database Token
        try:
            token_obj = Token.objects.select_related("user", "user__role").get(key=token_str)
            if not token_obj.user.is_active or token_obj.user.is_deleted:
                raise exceptions.AuthenticationFailed("User account is inactive or deleted.")
            return (token_obj.user, token_obj)
        except Token.DoesNotExist:
            pass

        raise exceptions.AuthenticationFailed("Your session has expired or is invalid. Please sign in again.")

    def authenticate_header(self, request):
        return 'Bearer realm="api"'

