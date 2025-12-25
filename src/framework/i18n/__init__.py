"""Internationalization (i18n) module for multi-language support.

This module provides comprehensive i18n support for the framework:
- Translation management with gettext
- Locale detection from request headers
- Dynamic language switching
- Pluralization support
- Date/time formatting per locale
- Number formatting per locale
- Currency formatting

Example:
    from framework.i18n import Translator, get_translator
    
    # Get translator for specific locale
    translator = get_translator("vi_VN")
    message = translator.translate("welcome_message", name="John")
    
    # Or use the translation function directly
    from framework.i18n import translate
    message = translate("en_US", "welcome_message", name="John")
"""

from framework.i18n.translator import Translator, get_translator, translate
from framework.i18n.locale import LocaleMiddleware, get_locale, set_locale

__all__ = [
    "Translator",
    "get_translator",
    "translate",
    "LocaleMiddleware",
    "get_locale",
    "set_locale",
]
