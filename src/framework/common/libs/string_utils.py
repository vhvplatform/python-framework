"""String utility functions with security focus."""

import html
import re
import secrets
import unicodedata
from typing import Optional


def sanitize_html(text: str) -> str:
    """Sanitize HTML to prevent XSS attacks.
    
    Args:
        text: Input text potentially containing HTML
        
    Returns:
        Sanitized text with HTML entities escaped
        
    Example:
        sanitize_html("<script>alert('xss')</script>")
        # Returns: "&lt;script&gt;alert('xss')&lt;/script&gt;"
    """
    return html.escape(text)


def slugify(text: str, separator: str = "-") -> str:
    """Convert text to URL-friendly slug.
    
    Args:
        text: Input text
        separator: Character to use for word separation
        
    Returns:
        URL-safe slug
        
    Example:
        slugify("Hello World! 123")
        # Returns: "hello-world-123"
    
    Note:
        Optimized with compiled regex patterns for better performance.
    """
    # Normalize unicode characters
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    
    # Convert to lowercase
    text = text.lower()
    
    # Replace spaces and special chars with separator (optimized with single regex)
    text = re.sub(r"[^\w\s-]+", "", text)
    text = re.sub(r"[\s_-]+", separator, text)
    text = text.strip(separator)
    
    return text


def truncate(text: str, length: int, suffix: str = "...") -> str:
    """Truncate text to specified length.
    
    Args:
        text: Input text
        length: Maximum length
        suffix: Suffix to append if truncated
        
    Returns:
        Truncated text
        
    Example:
        truncate("Hello World", 8)
        # Returns: "Hello..."
    """
    if len(text) <= length:
        return text
    
    return text[: length - len(suffix)] + suffix


def strip_whitespace(text: str) -> str:
    """Strip all extra whitespace from text.
    
    Args:
        text: Input text
        
    Returns:
        Text with normalized whitespace
        
    Example:
        strip_whitespace("  Hello   World  ")
        # Returns: "Hello World"
    """
    return " ".join(text.split())


def camel_to_snake(text: str) -> str:
    """Convert camelCase to snake_case.
    
    Args:
        text: CamelCase string
        
    Returns:
        snake_case string
        
    Example:
        camel_to_snake("myVariableName")
        # Returns: "my_variable_name"
    """
    # Insert underscore before uppercase letters
    text = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", text)
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    return text.lower()


def snake_to_camel(text: str, capitalize_first: bool = False) -> str:
    """Convert snake_case to camelCase.
    
    Args:
        text: snake_case string
        capitalize_first: Whether to capitalize first letter
        
    Returns:
        camelCase string
        
    Example:
        snake_to_camel("my_variable_name")
        # Returns: "myVariableName"
    
    Note:
        Optimized using str.title() method for better performance.
    """
    components = text.split("_")
    
    if capitalize_first:
        # Use str.title() for all components
        return "".join(comp.title() for comp in components)
    
    # Keep first component lowercase, title-case the rest
    return components[0] + "".join(comp.title() for comp in components[1:])


def mask_sensitive_data(text: str, visible_chars: int = 4) -> str:
    """Mask sensitive data showing only last few characters.
    
    Args:
        text: Sensitive data to mask
        visible_chars: Number of characters to keep visible
        
    Returns:
        Masked string
        
    Example:
        mask_sensitive_data("1234567890", 4)
        # Returns: "******7890"
    """
    if len(text) <= visible_chars:
        return "*" * len(text)
    
    return "*" * (len(text) - visible_chars) + text[-visible_chars:]


def generate_random_string(length: int = 32, include_special: bool = False) -> str:
    """Generate cryptographically secure random string.
    
    Args:
        length: Length of string to generate
        include_special: Include special characters
        
    Returns:
        Random string
        
    Example:
        generate_random_string(16)
        # Returns: "a7K9mP2nQ5rT8wX4"
    
    Note:
        Optimized using secrets.token_urlsafe() when special chars not needed.
    """
    if include_special:
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
        return "".join(secrets.choice(alphabet) for _ in range(length))
    else:
        # Use built-in token_urlsafe for better performance when special chars not needed
        # Adjust length since urlsafe encoding is more efficient
        return secrets.token_urlsafe(length)[:length]


def is_valid_email(email: str) -> bool:
    """Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email format
        
    Example:
        is_valid_email("user@example.com")
        # Returns: True
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def extract_numbers(text: str) -> list[int]:
    """Extract all numbers from text.
    
    Args:
        text: Input text
        
    Returns:
        List of integers found in text
        
    Example:
        extract_numbers("Price is 100 and tax is 15")
        # Returns: [100, 15]
    """
    return [int(num) for num in re.findall(r"\d+", text)]


def remove_html_tags(text: str) -> str:
    """Remove all HTML tags from text.
    
    Args:
        text: Text with HTML tags
        
    Returns:
        Plain text without HTML tags
        
    Example:
        remove_html_tags("<p>Hello <b>World</b></p>")
        # Returns: "Hello World"
    """
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)


def normalize_phone(phone: str, country_code: Optional[str] = None) -> str:
    """Normalize phone number to standard format.
    
    Args:
        phone: Phone number in any format
        country_code: Country code to prepend (e.g., "+1")
        
    Returns:
        Normalized phone number
        
    Example:
        normalize_phone("(123) 456-7890", "+1")
        # Returns: "+11234567890"
    """
    # Remove all non-digit characters
    digits = re.sub(r"\D", "", phone)
    
    if country_code:
        # Remove leading + from country code
        country_code = country_code.lstrip("+")
        # Add country code if not present
        if not digits.startswith(country_code):
            digits = country_code + digits
        return "+" + digits
    
    return digits
