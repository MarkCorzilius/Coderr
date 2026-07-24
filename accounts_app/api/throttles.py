from rest_framework.throttling import SimpleRateThrottle


class RegisterRateThrottle(SimpleRateThrottle):
    """Rate-limit registration attempts per IP."""

    scope = "register"

    def get_cache_key(self, request, view):
        """Return cache key based on client IP."""

        ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}


class LoginRateThrottle(SimpleRateThrottle):
    """Rate-limit login attempts per IP."""

    scope = "login"

    def get_cache_key(self, request, view):
        """Return cache key based on client IP."""

        ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}