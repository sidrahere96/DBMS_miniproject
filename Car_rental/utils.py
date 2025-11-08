"""
Utility functions for Car Rental System
"""
from datetime import datetime, timedelta
from typing import Tuple

def calculate_days(start_date: datetime, end_date: datetime) -> int:
    """Calculate number of days between two dates"""
    delta = end_date - start_date
    return max(1, delta.days)  # Minimum 1 day

def calculate_total_amount(daily_rate: float, start_date: datetime, end_date: datetime) -> float:
    """Calculate total rental amount"""
    days = calculate_days(start_date, end_date)
    return daily_rate * days

def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"₹{amount:,.2f}"

def format_date(date: datetime) -> str:
    """Format datetime to readable string"""
    return date.strftime("%d-%m-%Y")

def format_datetime(date: datetime) -> str:
    """Format datetime with time"""
    return date.strftime("%d-%m-%Y %I:%M %p")

def parse_date(date_str: str) -> datetime:
    """Parse date string to datetime"""
    try:
        return datetime.strptime(date_str, "%d-%m-%Y")
    except:
        return datetime.now()

def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number (Indian format)"""
    import re
    pattern = r'^[6-9]\d{9}$'
    return re.match(pattern, phone) is not None
