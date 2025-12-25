"""Security utility functions."""

import hashlib
import secrets
from typing import Optional

from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        True if password matches
    """
    return pwd_context.verify(plain_password, hashed_password)


def generate_token(length: int = 32) -> str:
    """Generate secure random token.
    
    Args:
        length: Token length in bytes
        
    Returns:
        Hex-encoded token
    """
    return secrets.token_hex(length)


def encrypt_data(data: str, key: Optional[str] = None) -> str:
    """Encrypt data (placeholder - use proper encryption library).
    
    Args:
        data: Data to encrypt
        key: Encryption key
        
    Returns:
        Encrypted data
    """
    # This is a placeholder - use proper encryption library like cryptography
    return hashlib.sha256(data.encode()).hexdigest()


def decrypt_data(encrypted: str, key: Optional[str] = None) -> str:
    """Decrypt data (placeholder - use proper encryption library).
    
    Args:
        encrypted: Encrypted data
        key: Decryption key
        
    Returns:
        Decrypted data
    """
    # This is a placeholder - use proper encryption library like cryptography
    return encrypted
