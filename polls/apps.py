"""Configuration django for polls application."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Poll app configuration."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
