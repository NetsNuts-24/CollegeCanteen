# accounts/apps.py
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'account'

    def ready(self):
        import account.models  # Ensure signals are registered
