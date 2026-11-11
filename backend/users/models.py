from django.db import models
from django.contrib.auth.models import AbstractUser
from populate_core.registry import register_model


@register_model("role", table_type="master")
class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255, blank=True, default="")
    is_superadmin = models.BooleanField(default=False, db_index=True)
    permission_version = models.PositiveIntegerField(default=1)
    status = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "roles"
        indexes = [
            models.Index(fields=["status", "created_at"]),
        ]

    def __str__(self):
        return self.name


@register_model("user", table_type="master", aliases=["users"])
class User(AbstractUser):
    name = models.CharField(max_length=150, blank=True, default="")
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    status = models.SmallIntegerField(default=1)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["role", "status"]),
        ]

    def __str__(self):
        return self.username

    @property
    def is_superadmin(self):
        if self.is_superuser:
            return True
        if self.role and getattr(self.role, "is_superadmin", False):
            return True
        return False

