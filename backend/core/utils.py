"""
Utility Functions
Helper functions used across the application

TODO: Contributors add utility functions as needed
"""

import hashlib
import json
from datetime import datetime
from typing import Any, Dict, List
import re


def generate_id(prefix: str = "rec") -> str:
    """
    Generate a unique ID with timestamp
    
    TODO: Implement proper UUID or database ID generation
    
    Args:
        prefix: Prefix for the ID
        
    Returns:
        Unique identifier string
    """
    timestamp = datetime.utcnow().isoformat()
    hash_input = f"{prefix}_{timestamp}".encode()
    return f"{prefix}_{hashlib.md5(hash_input).hexdigest()[:8]}"


def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    TODO: Implement text cleaning logic
    - Remove special characters
    - Normalize whitespace
    - Handle encoding issues
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', text).strip()
    return cleaned


def extract_email(text: str) -> str | None:
    """
    Extract email from text
    
    TODO: Implement robust email extraction
    
    Args:
        text: Text containing email
        
    Returns:
        Email address or None
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    """
    Extract phone number from text
    
    TODO: Implement phone extraction with multiple formats
    
    Args:
        text: Text containing phone
        
    Returns:
        Phone number or None
    """
    # Basic pattern - enhance as needed
    phone_pattern = r'\b\d{10}\b|\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    match = re.search(phone_pattern, text)
    return match.group(0) if match else None


def parse_date(date_str: str) -> datetime | None:
    """
    Parse date string to datetime
    
    TODO: Handle multiple date formats
    
    Args:
        date_str: Date string
        
    Returns:
        Datetime object or None
    """
    try:
        return datetime.fromisoformat(date_str)
    except:
        return None


def calculate_experience_years(experiences: List[Dict[str, Any]]) -> float:
    """
    Calculate total years of experience
    
    TODO: Implement logic to calculate experience from resume data
    
    Args:
        experiences: List of experience entries
        
    Returns:
        Total years of experience
    """
    # Placeholder implementation
    return 0.0


def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Format currency amount
    
    Args:
        amount: Amount to format
        currency: Currency code
        
    Returns:
        Formatted currency string
    """
    return f"{currency} {amount:,.2f}"


def validate_json(data: str) -> bool:
    """
    Validate if string is valid JSON
    
    Args:
        data: JSON string
        
    Returns:
        True if valid JSON
    """
    try:
        json.loads(data)
        return True
    except:
        return False


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove special characters
    safe_name = re.sub(r'[^\w\s.-]', '', filename)
    return safe_name.strip()
