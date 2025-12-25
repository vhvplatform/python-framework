"""Date and time utility functions."""

from datetime import datetime, timezone
from typing import Optional
import re


def parse_datetime(date_str: str, format_str: Optional[str] = None) -> datetime:
    """Parse datetime from string.
    
    Args:
        date_str: Date string to parse
        format_str: Optional format string (auto-detects if None)
        
    Returns:
        Parsed datetime object
    """
    if format_str:
        return datetime.strptime(date_str, format_str)
    
    # Try common formats
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Could not parse date string: {date_str}")


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime to string.
    
    Args:
        dt: Datetime object
        format_str: Format string
        
    Returns:
        Formatted datetime string
    """
    return dt.strftime(format_str)


def get_timezone(tz_name: str = "UTC") -> timezone:
    """Get timezone object.
    
    Args:
        tz_name: Timezone name
        
    Returns:
        Timezone object
    """
    return timezone.utc


def convert_timezone(dt: datetime, target_tz: timezone) -> datetime:
    """Convert datetime to different timezone.
    
    Args:
        dt: Datetime to convert
        target_tz: Target timezone
        
    Returns:
        Converted datetime
    """
    return dt.astimezone(target_tz)


def is_valid_date(date_str: str) -> bool:
    """Check if string is valid date.
    
    Args:
        date_str: Date string to validate
        
    Returns:
        True if valid date
    """
    try:
        parse_datetime(date_str)
        return True
    except ValueError:
        return False
