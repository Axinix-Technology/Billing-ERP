import logging
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from populate_core.registry import BaseService, register_service

logger = logging.getLogger(__name__)


@register_service("role")
class RoleService(BaseService):
    def check_permission(self, context):
        # Defer authorization cleanly to PolicyEngine (is_superadmin + DB-backed AccessPolicy)
        return None

    def get_policy_scope(self, context):
        if getattr(context, "is_superadmin", False):
            return Q()
        return Q(status=1)


@register_service("user")
class UserService(BaseService):
    def check_permission(self, context):
        # Defer authorization cleanly to PolicyEngine (is_superadmin + DB-backed AccessPolicy)
        return None

    def get_policy_scope(self, context):
        if getattr(context, "is_superadmin", False):
            return Q()
        return Q(is_deleted=False, status=1)

    def before_create(self, context, data):
        password = data.get("password")
        if password:
            data["password"] = make_password(password)
        return data

    def before_update(self, context, instance, data):
        password = data.get("password")
        if password:
            data["password"] = make_password(password)
        else:
            data.pop("password", None)
        return data
