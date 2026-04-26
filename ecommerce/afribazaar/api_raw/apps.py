"""
API Raw App Configuration
Database-first REST API that exposes raw SQL tables
"""

from django.apps import AppConfig


class ApiRawConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_raw'
    verbose_name = 'Raw SQL API'
