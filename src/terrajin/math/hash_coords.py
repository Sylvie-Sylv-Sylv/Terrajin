def hash_coords(seed: int, primed_grid_x: int, primed_grid_y: int) -> int:
    """
    Computes the hash for a lattice coordinate.

    Mirrors the FastNoiseLite implementation.
    """

    hash_value = seed ^ primed_grid_x ^ primed_grid_y

    # Simulate 32-bit signed integer overflow
    hash_value = (hash_value * 0x27D4EB2D) & 0xFFFFFFFF

    return hash_value