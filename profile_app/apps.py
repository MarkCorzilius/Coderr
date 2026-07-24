from django.apps import AppConfig


class ProfileAppConfig(AppConfig):
    """App config for profile_app; loads signals on ready."""

    name = "profile_app"

    def ready(self):
        """Import signals to register post-save handler."""

        import profile_app.signals  # noqa: F401
