import numpy as np
import matplotlib.pyplot as plt

from terrajin.math.noise.gradient_noise.perlin_noise import PerlinNoise2D

# Parameters
WIDTH = 512
HEIGHT = 512
SCALE = 16.0
SEED = 1337

image = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

noise_gen = PerlinNoise2D(SEED)

for y in range(HEIGHT):
    for x in range(WIDTH):
        image[y, x] = noise_gen(
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
plt.title("Perlin Noise")
plt.tight_layout()
plt.show()