import unittest

import numpy as np
from PIL import Image

from modules.rendering import _create_gif


class RenderingTests(unittest.TestCase):
    def test_creates_animated_gif_in_memory(self):
        memory = np.zeros((3, 1, 8, 8))

        gif = Image.open(_create_gif(memory))

        self.assertEqual(gif.n_frames, 3)


if __name__ == "__main__":
    unittest.main()
