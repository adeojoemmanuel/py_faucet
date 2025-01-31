# faucet/apps.py
from django.apps import AppConfig

class FaucetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'faucet'  # <-- Match the app directory name