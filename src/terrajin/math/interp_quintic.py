def interp_quintic(t: float) -> float:
    """
    Quintic interpolation function for smooth transitions.
    This function is used to compute the interpolation weights for Perlin noise.
    """
    return t * t * t * (t * (t * 6 - 15) + 10)