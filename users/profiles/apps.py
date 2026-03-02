from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'users.profiles'
    label = 'users_profiles'

    def ready(self):
        from . import signals
