"""
Alias command for seed_users.
Allows developers and testers to invoke `python manage.py seed_user_credentials`
interchangeably with `python manage.py seed_users`.
"""
from users.management.commands.seed_users import Command

__all__ = ["Command"]

