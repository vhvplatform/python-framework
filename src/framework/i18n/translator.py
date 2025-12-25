"""Translation manager with support for multiple languages."""

import json
from pathlib import Path
from typing import Any, Dict, Optional

from framework.observability.logging import get_logger

logger = get_logger(__name__)


class Translator:
    """Translator for handling multi-language support.
    
    Provides translation capabilities with:
    - Template variable substitution
    - Fallback to default language
    - Pluralization support
    - Nested key access with dot notation
    
    Example:
        translator = Translator("vi_VN", translations)
        message = translator.translate("user.welcome", name="John")
    """

    def __init__(
        self,
        locale: str,
        translations: Dict[str, Any],
        default_locale: str = "en_US",
    ) -> None:
        """Initialize translator.
        
        Args:
            locale: Target locale code (e.g., 'en_US', 'vi_VN')
            translations: Translation dictionary
            default_locale: Fallback locale if translation not found
        """
        self.locale = locale
        self.translations = translations
        self.default_locale = default_locale

    def translate(self, key: str, **kwargs: Any) -> str:
        """Translate a key to the target language.
        
        Args:
            key: Translation key (supports dot notation: 'user.welcome')
            **kwargs: Variables for template substitution
            
        Returns:
            Translated string with variables substituted
            
        Example:
            translator.translate("user.welcome", name="John")
            # Returns: "Welcome, John!"
        """
        # Try to get translation for current locale
        translation = self._get_nested_value(self.translations.get(self.locale, {}), key)
        
        # Fallback to default locale if not found
        if translation is None and self.locale != self.default_locale:
            translation = self._get_nested_value(
                self.translations.get(self.default_locale, {}), key
            )
        
        # If still not found, return the key itself
        if translation is None:
            logger.warning(
                "Translation not found",
                key=key,
                locale=self.locale,
                default_locale=self.default_locale,
            )
            return key
        
        # Substitute variables
        try:
            return translation.format(**kwargs)
        except KeyError as e:
            logger.error("Missing variable in translation", key=key, error=str(e))
            return translation

    def translate_plural(
        self,
        key: str,
        count: int,
        **kwargs: Any,
    ) -> str:
        """Translate with pluralization support.
        
        Args:
            key: Translation key (should have 'zero', 'one', 'other' variants)
            count: Number for pluralization
            **kwargs: Variables for template substitution
            
        Returns:
            Translated string with proper plural form
            
        Example:
            translator.translate_plural("items.count", count=5)
            # Returns: "You have 5 items"
        """
        # Determine plural form
        if count == 0:
            plural_key = f"{key}.zero"
        elif count == 1:
            plural_key = f"{key}.one"
        else:
            plural_key = f"{key}.other"
        
        return self.translate(plural_key, count=count, **kwargs)

    def _get_nested_value(self, data: Dict[str, Any], key: str) -> Optional[str]:
        """Get value from nested dictionary using dot notation.
        
        Args:
            data: Dictionary to search
            key: Dot-separated key path (e.g., 'user.profile.name')
            
        Returns:
            Value if found, None otherwise
        """
        keys = key.split(".")
        value: Any = data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        
        return str(value) if value is not None else None


class TranslationLoader:
    """Loader for translation files from JSON."""

    def __init__(self, translations_dir: Path) -> None:
        """Initialize translation loader.
        
        Args:
            translations_dir: Directory containing translation JSON files
        """
        self.translations_dir = translations_dir
        self._cache: Dict[str, Dict[str, Any]] = {}

    def load_translations(self) -> Dict[str, Any]:
        """Load all translation files from directory.
        
        Returns:
            Dictionary mapping locale codes to translations
            
        Example:
            {
                "en_US": {"welcome": "Welcome", ...},
                "vi_VN": {"welcome": "Chào mừng", ...}
            }
        """
        translations: Dict[str, Any] = {}
        
        if not self.translations_dir.exists():
            logger.warning(
                "Translations directory not found",
                path=str(self.translations_dir),
            )
            return translations
        
        for file_path in self.translations_dir.glob("*.json"):
            locale = file_path.stem
            
            try:
                with open(file_path, encoding="utf-8") as f:
                    translations[locale] = json.load(f)
                    logger.info("Loaded translations", locale=locale, file=file_path.name)
            except Exception as e:
                logger.error(
                    "Failed to load translations",
                    locale=locale,
                    file=file_path.name,
                    error=str(e),
                )
        
        self._cache = translations
        return translations

    def reload(self) -> Dict[str, Any]:
        """Reload translations from disk.
        
        Returns:
            Updated translations dictionary
        """
        return self.load_translations()


# Global translation storage
_translations: Dict[str, Any] = {}
_default_locale = "en_US"


def initialize_translations(translations_dir: Path, default_locale: str = "en_US") -> None:
    """Initialize translation system.
    
    Args:
        translations_dir: Directory containing translation JSON files
        default_locale: Default locale code
    """
    global _translations, _default_locale
    
    loader = TranslationLoader(translations_dir)
    _translations = loader.load_translations()
    _default_locale = default_locale
    
    logger.info(
        "Initialized translations",
        locales=list(_translations.keys()),
        default_locale=default_locale,
    )


def get_translator(locale: str) -> Translator:
    """Get translator for specific locale.
    
    Args:
        locale: Target locale code
        
    Returns:
        Translator instance
    """
    return Translator(locale, _translations, _default_locale)


def translate(locale: str, key: str, **kwargs: Any) -> str:
    """Translate a key for specific locale.
    
    Args:
        locale: Target locale code
        key: Translation key
        **kwargs: Variables for substitution
        
    Returns:
        Translated string
    """
    translator = get_translator(locale)
    return translator.translate(key, **kwargs)
