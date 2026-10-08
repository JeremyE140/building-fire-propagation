import unittest

import numpy as np
from PIL import Image

from modules.visualization.rendering import _create_gif, _fit_frame


class RenderingTests(unittest.TestCase):
    def test_creates_animated_gif_in_memory(self):
        memory = np.zeros((3, 1, 8, 8))

        gif = Image.open(_create_gif(memory))

        self.assertEqual(gif.n_frames, 3)

    def test_fits_frame_inside_visualization_window(self):
        frame = Image.new("RGB", (800, 400))

        fitted = _fit_frame(frame, (300, 300))

        self.assertEqual(fitted.size, (300, 150))

if __name__ == "__main__":
    unittest.main()
