from django.apps import AppConfig


class ProfilesAppConfig(AppConfig):
    """App config for profiles_app; loads signals on ready."""

    name = "profiles_app"

    def ready(self):
        """Import signals to register post-save handler."""

        import profiles_app.signals  # noqa: F401
