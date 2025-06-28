from datetime import timedelta

def utc_to_ist(dt):
    """Convert a UTC datetime to IST (Indian Standard Time)."""
    if dt is None:
        return None
    return dt + timedelta(hours=5, minutes=30)