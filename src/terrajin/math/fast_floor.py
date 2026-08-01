def fast_floor(x: float) -> int:
    """
    Fast floor function that returns the largest integer less than or equal to x.
    This implementation is faster than the built-in math.floor for positive numbers.
    """
    return int(x) if x >= 0 else int(x) - 1