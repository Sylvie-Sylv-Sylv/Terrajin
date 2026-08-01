import math

from terrajin.math.constants import PRIME_X, PRIME_Y
from terrajin.math.fast_floor import fast_floor
from terrajin.math.gradient_dot import gradient_dot
from terrajin.math.interp_quintic import interp_quintic
from terrajin.math.lerp import lerp


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