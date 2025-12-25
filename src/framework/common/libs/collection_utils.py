"""Collection utility functions."""

from typing import Any, Callable, Iterable, List, Dict, TypeVar, Optional

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


def chunk_list(items: List[T], chunk_size: int) -> List[List[T]]:
    """Split list into chunks.
    
    Args:
        items: List to chunk
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]


def flatten_list(nested_list: List[List[T]]) -> List[T]:
    """Flatten nested list.
    
    Args:
        nested_list: Nested list structure
        
    Returns:
        Flattened list
    """
    return [item for sublist in nested_list for item in sublist]


def group_by(items: Iterable[T], key_func: Callable[[T], K]) -> Dict[K, List[T]]:
    """Group items by key function.
    
    Args:
        items: Items to group
        key_func: Function to extract grouping key
        
    Returns:
        Dictionary of grouped items
    """
    result: Dict[K, List[T]] = {}
    for item in items:
        key = key_func(item)
        if key not in result:
            result[key] = []
        result[key].append(item)
    return result


def deduplicate(items: List[T]) -> List[T]:
    """Remove duplicates while preserving order.
    
    Args:
        items: List with possible duplicates
        
    Returns:
        List without duplicates
    """
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def safe_get(dictionary: Dict[K, V], key: K, default: Optional[V] = None) -> Optional[V]:
    """Safely get value from dictionary.
    
    Args:
        dictionary: Dictionary to query
        key: Key to lookup
        default: Default value if key not found
        
    Returns:
        Value or default
    """
    return dictionary.get(key, default)
