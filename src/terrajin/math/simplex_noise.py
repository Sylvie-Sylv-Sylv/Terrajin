import math

from terrajin.math.constants import PRIME_X, PRIME_Y, SIMPLEX_G2, SIMPLEX_F2
from terrajin.math.fast_floor import fast_floor
from terrajin.math.gradient_dot import gradient_dot


def simplex_noise_2d(seed: int, x: float, y: float) -> float:
    # ------------------------------------------------------------------
    # Skew input (normally done outside SingleSimplex in FastNoiseLite)
    # ------------------------------------------------------------------
    skew = (x + y) * SIMPLEX_F2
    x += skew
    y += skew

    # ------------------------------------------------------------------
    # Determine simplex cell
    # ------------------------------------------------------------------
    cell_x = fast_floor(x)
    cell_y = fast_floor(y)

    frac_x = x - cell_x
    frac_y = y - cell_y

    unskew = (frac_x + frac_y) * SIMPLEX_G2

    corner0_x = frac_x - unskew
    corner0_y = frac_y - unskew

    # Prime coordinates for hashing
    cell_x *= PRIME_X
    cell_y *= PRIME_Y

    # ------------------------------------------------------------------
    # Corner 0
    # ------------------------------------------------------------------
    a = 0.5 - corner0_x * corner0_x - corner0_y * corner0_y

    if a <= 0.0:
        n0 = 0.0
    else:
        a2 = a * a
        n0 = a2 * a2 * gradient_dot(
            seed,
            cell_x,
            cell_y,
            corner0_x,
            corner0_y,
        )

    # ------------------------------------------------------------------
    # Corner 2
    # ------------------------------------------------------------------
    c = (
        (2.0 * (1.0 - 2.0 * SIMPLEX_G2) * (1.0 / SIMPLEX_G2 - 2.0)) * unskew
        + (-2.0 * (1.0 - 2.0 * SIMPLEX_G2) * (1.0 - 2.0 * SIMPLEX_G2) + a)
    )

    if c <= 0.0:
        n2 = 0.0
    else:
        corner2_x = corner0_x + (2.0 * SIMPLEX_G2 - 1.0)
        corner2_y = corner0_y + (2.0 * SIMPLEX_G2 - 1.0)

        c2 = c * c

        n2 = c2 * c2 * gradient_dot(
            seed,
            cell_x + PRIME_X,
            cell_y + PRIME_Y,
            corner2_x,
            corner2_y,
        )

    # ------------------------------------------------------------------
    # Corner 1
    # ------------------------------------------------------------------
    if corner0_y > corner0_x:

        corner1_x = corner0_x + SIMPLEX_G2
        corner1_y = corner0_y + (SIMPLEX_G2 - 1.0)

        b = 0.5 - corner1_x * corner1_x - corner1_y * corner1_y

        if b <= 0.0:
            n1 = 0.0
        else:
            b2 = b * b

            n1 = b2 * b2 * gradient_dot(
                seed,
                cell_x,
                cell_y + PRIME_Y,
                corner1_x,
                corner1_y,
            )

    else:

        corner1_x = corner0_x + (SIMPLEX_G2 - 1.0)
        corner1_y = corner0_y + SIMPLEX_G2

        b = 0.5 - corner1_x * corner1_x - corner1_y * corner1_y

        if b <= 0.0:
            n1 = 0.0
        else:
            b2 = b * b

            n1 = b2 * b2 * gradient_dot(
                seed,
                cell_x + PRIME_X,
                cell_y,
                corner1_x,
                corner1_y,
            )

    return (n0 + n1 + n2) * 99.83685446303647