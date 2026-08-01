from terrajin.math.constants import GRADIENTS_2D
from terrajin.math.hash_coords import hash_coords


def gradient_dot(seed: int,
                 primed_grid_x: int,
                 primed_grid_y: int,
                 offset_x: float,
                 offset_y: float) -> float:
    """
    Computes the dot product between the selected gradient vector
    and the displacement from the lattice point.
    """

    hash_value = hash_coords(seed, primed_grid_x, primed_grid_y)
    hash_value ^= hash_value >> 15
    hash_value &= 127 << 1

    gradient_x = GRADIENTS_2D[hash_value]
    gradient_y = GRADIENTS_2D[hash_value | 1]

    return offset_x * gradient_x + offset_y * gradient_y