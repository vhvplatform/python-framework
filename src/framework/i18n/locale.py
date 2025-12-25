"""Locale detection and management middleware."""

from contextvars import ContextVar
from typing import Callable, List, Optional

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from framework.observability.logging import get_logger

logger = get_logger(__name__)

# Context variable for storing current locale
_current_locale: ContextVar[str] = ContextVar("current_locale", default="en_US")


def get_locale() -> str:
    """Get current request locale.
    
    Returns:
        Current locale code (e.g., 'en_US', 'vi_VN')
    """
    return _current_locale.get()


def set_locale(locale: str) -> None:
    """Set current request locale.
    
    Args:
        locale: Locale code to set
    """
    _current_locale.set(locale)


class LocaleMiddleware(BaseHTTPMiddleware):
    """Middleware for automatic locale detection from request.
    
    Detects locale from:
    1. Query parameter 'locale' or 'lang'
    2. Cookie 'locale'
    3. Accept-Language header
    4. Default locale
    
    Example:
        app.add_middleware(
            LocaleMiddleware,
            default_locale="en_US",
            supported_locales=["en_US", "vi_VN", "ja_JP"]
        )
    """

    def __init__(
        self,
        app: ASGIApp,
        default_locale: str = "en_US",
        supported_locales: Optional[List[str]] = None,
    ) -> None:
        """Initialize locale middleware.
        
        Args:
            app: ASGI application
            default_locale: Default locale if detection fails
            supported_locales: List of supported locale codes
        """
        super().__init__(app)
        self.default_locale = default_locale
        self.supported_locales = supported_locales or [default_locale]

    async def dispatch(self, request: Request, call_next: Callable) -> any:  # type: ignore[misc]
        """Process request and detect locale.
        
        Args:
            request: HTTP request
            call_next: Next middleware/handler
            
        Returns:
            HTTP response
        """
        locale = self._detect_locale(request)
        set_locale(locale)
        
        logger.debug("Detected locale", locale=locale, path=request.url.path)
        
        response = await call_next(request)
        
        # Set locale cookie if not present
        if "locale" not in request.cookies:
            response.set_cookie(
                key="locale",
                value=locale,
                max_age=365 * 24 * 60 * 60,  # 1 year
                httponly=True,
                samesite="lax",
            )
        
        return response

    def _detect_locale(self, request: Request) -> str:
        """Detect locale from request.
        
        Args:
            request: HTTP request
            
        Returns:
            Detected locale code
        """
        # 1. Check query parameters
        locale = request.query_params.get("locale") or request.query_params.get("lang")
        if locale and self._is_supported(locale):
            return locale
        
        # 2. Check cookie
        locale = request.cookies.get("locale")
        if locale and self._is_supported(locale):
            return locale
        
        # 3. Check Accept-Language header
        accept_language = request.headers.get("Accept-Language")
        if accept_language:
            locale = self._parse_accept_language(accept_language)
            if locale:
                return locale
        
        # 4. Return default
        return self.default_locale

    def _is_supported(self, locale: str) -> bool:
        """Check if locale is supported.
        
        Args:
            locale: Locale code to check
            
        Returns:
            True if supported
        """
        return locale in self.supported_locales

    def _parse_accept_language(self, accept_language: str) -> Optional[str]:
        """Parse Accept-Language header and return best match.
        
        Args:
            accept_language: Accept-Language header value
            
        Returns:
            Best matching locale code or None
        """
        # Parse header: "en-US,en;q=0.9,vi;q=0.8"
        languages = []
        
        for lang_part in accept_language.split(","):
            parts = lang_part.strip().split(";")
            lang = parts[0].strip()
            
            # Get quality value (default 1.0)
            quality = 1.0
            if len(parts) > 1:
                try:
                    q_value = parts[1].strip()
                    if q_value.startswith("q="):
                        quality = float(q_value[2:])
                except (ValueError, IndexError):
                    pass
            
            languages.append((lang, quality))
        
        # Sort by quality (highest first)
        languages.sort(key=lambda x: x[1], reverse=True)
        
        # Find first supported locale
        for lang, _ in languages:
            # Convert 'en-US' to 'en_US'
            locale = lang.replace("-", "_")
            
            if self._is_supported(locale):
                return locale
            
            # Try language prefix (e.g., 'en' from 'en-GB')
            if "_" in locale or "-" in lang:
                lang_prefix = lang.split("-")[0] + "_"
                for supported in self.supported_locales:
                    if supported.startswith(lang_prefix):
                        return supported
        
        return None
