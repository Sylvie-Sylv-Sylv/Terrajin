import numpy as np
import matplotlib.pyplot as plt

from terrajin.math.open_simplex2s_noise import open_simplex2s_noise_2d

# Parameters
WIDTH = 512
HEIGHT = 512
SCALE = 64.0
SEED = 1337

image = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

for y in range(HEIGHT):
    for x in range(WIDTH):
        image[y, x] = open_simplex2s_noise_2d(
            SEED,
            x / SCALE,
            y / SCALE,
        )

plt.figure(figsize=(8, 8))
plt.imshow(
    image,
    cmap="gray",
    origin="lower",
    interpolation="nearest",
)
plt.colorbar(label="Noise Value")
plt.title("OpenSimplex2s Noise")
plt.tight_layout()
plt.show()