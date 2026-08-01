from terrajin.math.constants import PRIME_X, PRIME_Y, PRIME_Y, SIMPLEX_F2, SIMPLEX_G2
from terrajin.math.fast_floor import fast_floor
from terrajin.math.gradient_dot import gradient_dot


def open_simplex2s_noise_2d(seed: int, x: float, y: float) -> float:
    # ------------------------------------------------------------------
    # Skew input coordinates (normally done before calling in FastNoiseLite)
    # ------------------------------------------------------------------
    skew = (x + y) * SIMPLEX_F2
    x += skew
    y += skew

    # ------------------------------------------------------------------
    # Cell coordinates
    # ------------------------------------------------------------------
    cell_x = fast_floor(x)
    cell_y = fast_floor(y)

    frac_x = x - cell_x
    frac_y = y - cell_y

    hash_x = cell_x * PRIME_X
    hash_y = cell_y * PRIME_Y

    hash_x1 = hash_x + PRIME_X
    hash_y1 = hash_y + PRIME_Y

    # ------------------------------------------------------------------
    # Unskew
    # ------------------------------------------------------------------
    t = (frac_x + frac_y) * SIMPLEX_G2

    x0 = frac_x - t
    y0 = frac_y - t

    # ------------------------------------------------------------------
    # First corner
    # ------------------------------------------------------------------
    a0 = (2.0 / 3.0) - x0 * x0 - y0 * y0

    value = (
        a0 * a0 * a0 * a0
        * gradient_dot(seed, hash_x, hash_y, x0, y0)
    )

    # ------------------------------------------------------------------
    # Second corner
    # ------------------------------------------------------------------
    a1 = (
        (2.0 * (1.0 - 2.0 * SIMPLEX_G2) * (1.0 / SIMPLEX_G2 - 2.0)) * t
        + (-2.0 * (1.0 - 2.0 * SIMPLEX_G2) * (1.0 - 2.0 * SIMPLEX_G2) + a0)
    )

    x1 = x0 - (1.0 - 2.0 * SIMPLEX_G2)
    y1 = y0 - (1.0 - 2.0 * SIMPLEX_G2)

    value += (
        a1 * a1 * a1 * a1
        * gradient_dot(seed, hash_x1, hash_y1, x1, y1)
    )

    # ------------------------------------------------------------------
    # Remaining two corners
    # ------------------------------------------------------------------
    x_minus_y = frac_x - frac_y

    if t > SIMPLEX_G2:

        if frac_x + x_minus_y > 1.0:
            x2 = x0 + (3.0 * SIMPLEX_G2 - 2.0)
            y2 = y0 + (3.0 * SIMPLEX_G2 - 1.0)

            a2 = (2.0 / 3.0) - x2 * x2 - y2 * y2

            if a2 > 0.0:
                value += (
                    a2 * a2 * a2 * a2
                    * gradient_dot(
                        seed,
                        hash_x + (PRIME_X << 1),
                        hash_y + PRIME_Y,
                        x2,
                        y2,
                    )
                )

        else:
            x2 = x0 + SIMPLEX_G2
            y2 = y0 + (SIMPLEX_G2 - 1.0)

            a2 = (2.0 / 3.0) - x2 * x2 - y2 * y2

            if a2 > 0.0:
                value += (
                    a2 * a2 * a2 * a2
                    * gradient_dot(
                        seed,
                        hash_x,
                        hash_y + PRIME_Y,
                        x2,
                        y2,
                    )
                )

        if frac_y - x_minus_y > 1.0:
            x3 = x0 + (3.0 * SIMPLEX_G2 - 1.0)
            y3 = y0 + (3.0 * SIMPLEX_G2 - 2.0)

            a3 = (2.0 / 3.0) - x3 * x3 - y3 * y3

            if a3 > 0.0:
                value += (
                    a3 * a3 * a3 * a3
                    * gradient_dot(
                        seed,
                        hash_x + PRIME_X,
                        hash_y + (PRIME_Y << 1),
                        x3,
                        y3,
                    )
                )

        else:
            x3 = x0 + (SIMPLEX_G2 - 1.0)
            y3 = y0 + SIMPLEX_G2

            a3 = (2.0 / 3.0) - x3 * x3 - y3 * y3

            if a3 > 0.0:
                value += (
                    a3 * a3 * a3 * a3
                    * gradient_dot(
                        seed,
                        hash_x + PRIME_X,
                        hash_y,
                        x3,
                        y3,
                    )
                )

    else:

        if frac_x + x_minus_y < 0.0:
            x2 = x0 + (1.0 - SIMPLEX_G2)
            y2 = y0 - SIMPLEX_G2

            a2 = (2.0 / 3.0) - x2 * x2 - y2 * y2

            if a2 > 0.0:
                value += (
                    a2 * a2 * a2 * a2
                    * gradient_dot(
                        seed,
                        hash_x - PRIME_X,
                        hash_y,
                        x2,
                        y2,
                    )
                )

        else:
            x2 = x0 + (SIMPLEX_G2 - 1.0)
            y2 = y0 + SIMPLEX_G2

            a2 = (2.0 / 3.0) - x2 * x2 - y2 * y2

            if a2 > 0.0:
                value += (
                    a2 * a2 * a2 * a2
                    * gradient_dot(
                        seed,
                        hash_x + PRIME_X,
                        hash_y,
                        x2,
                        y2,
                    )
                )

        if frac_y < x_minus_y:
            x3 = x0 - SIMPLEX_G2
            y3 = y0 - (SIMPLEX_G2 - 1.0)

            a3 = (2.0 / 3.0) - x3 * x3 - y3 * y3

            if a3 > 0.0:
                value += (
                    a3 * a3 * a3 * a3
                    * gradient_dot(
                        seed,
                        hash_x,
                        hash_y - PRIME_Y,
                        x3,
                        y3,
                    )
                )

        else:
            x3 = x0 + SIMPLEX_G2
            y3 = y0 + (SIMPLEX_G2 - 1.0)

            a3 = (2.0 / 3.0) - x3 * x3 - y3 * y3

            if a3 > 0.0:
                value += (
                    a3 * a3 * a3 * a3
                    * gradient_dot(
                        seed,
                        hash_x,
                        hash_y + PRIME_Y,
                        x3,
                        y3,
                    )
                )

    return value * 18.24196194486065