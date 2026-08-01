import math

from terrajin.math.fast_floor import fast_floor
from terrajin.math.interp_quintic import interp_quintic
from terrajin.math.lerp import lerp

PRIME_X: int = 501125321
PRIME_Y: int = 1136930381
PRIME_Z: int = 1720413743

GRADIENTS_2D = (
     0.130526192220052,  0.991444861373810,
     0.382683432365090,  0.923879532511287,
     0.608761429008721,  0.793353340291235,
     0.793353340291235,  0.608761429008721,
     0.923879532511287,  0.382683432365090,
     0.991444861373810,  0.130526192220051,
     0.991444861373810, -0.130526192220051,
     0.923879532511287, -0.382683432365090,
     0.793353340291235, -0.608761429008720,
     0.608761429008721, -0.793353340291235,
     0.382683432365090, -0.923879532511287,
     0.130526192220052, -0.991444861373810,
    -0.130526192220052, -0.991444861373810,
    -0.382683432365090, -0.923879532511287,
    -0.608761429008721, -0.793353340291235,
    -0.793353340291235, -0.608761429008721,
    -0.923879532511287, -0.382683432365090,
    -0.991444861373810, -0.130526192220052,
    -0.991444861373810,  0.130526192220051,
    -0.923879532511287,  0.382683432365090,
    -0.793353340291235,  0.608761429008721,
    -0.608761429008721,  0.793353340291235,
    -0.382683432365090,  0.923879532511287,
    -0.130526192220052,  0.991444861373810,

    # The above 48 values are repeated several times in FastNoiseLite.
    # For Python, it's cleaner to generate the repetitions:
) * 6 + (
     0.382683432365090,  0.923879532511287,
     0.923879532511287,  0.382683432365090,
     0.923879532511287, -0.382683432365090,
     0.382683432365090, -0.923879532511287,
    -0.382683432365090, -0.923879532511287,
    -0.923879532511287, -0.382683432365090,
    -0.923879532511287,  0.382683432365090,
    -0.382683432365090,  0.923879532511287,
)

def hash_coords(seed: int, primed_grid_x: int, primed_grid_y: int) -> int:
    """
    Computes the hash for a lattice coordinate.

    Mirrors the FastNoiseLite implementation.
    """

    hash_value = seed ^ primed_grid_x ^ primed_grid_y

    # Simulate 32-bit signed integer overflow
    hash_value = (hash_value * 0x27D4EB2D) & 0xFFFFFFFF

    return hash_value


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


def perlin_noise_2d(seed: int, x: float, y: float) -> float:
    """
    Computes one octave of 2D Perlin noise.
    """

    # Integer lattice coordinates
    cell_x = fast_floor(x)
    cell_y = fast_floor(y)

    # Position inside the cell
    local_x = x - cell_x
    local_y = y - cell_y

    # Offsets to neighboring lattice points
    local_x_next = local_x - 1.0
    local_y_next = local_y - 1.0

    # Smooth interpolation weights
    weight_x = interp_quintic(local_x)
    weight_y = interp_quintic(local_y)

    # Prime the lattice coordinates for hashing
    lattice_x0 = cell_x * PRIME_X
    lattice_y0 = cell_y * PRIME_Y

    lattice_x1 = lattice_x0 + PRIME_X
    lattice_y1 = lattice_y0 + PRIME_Y

    # Gradient contributions
    bottom_left = gradient_dot(
        seed,
        lattice_x0,
        lattice_y0,
        local_x,
        local_y,
    )

    bottom_right = gradient_dot(
        seed,
        lattice_x1,
        lattice_y0,
        local_x_next,
        local_y,
    )

    top_left = gradient_dot(
        seed,
        lattice_x0,
        lattice_y1,
        local_x,
        local_y_next,
    )

    top_right = gradient_dot(
        seed,
        lattice_x1,
        lattice_y1,
        local_x_next,
        local_y_next,
    )

    # Bilinear interpolation
    bottom = lerp(bottom_left, bottom_right, weight_x)
    top = lerp(top_left, top_right, weight_x)

    return lerp(bottom, top, weight_y) * 1.4247691104677813