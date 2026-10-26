def normalize_shift_type(value):
    """Return the canonical shift type for API input and filter values."""
    normalized = str(value).strip().lower()
    if normalized == "basic":
        return "general"
    return normalized
